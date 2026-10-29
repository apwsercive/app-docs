"""Read Markdown documents; bundled parser keeps builds offline and portable."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
from markdown_it import MarkdownIt


def read_markdown(source, content_root, base):
    text = source.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    metadata = {}
    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise ValueError(f"Unclosed document metadata: {source}")
        for line in lines[1:end]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, separator, value = line.partition(":")
            if not separator or key not in ("title", "version", "updated", "effective", "status") or key in metadata:
                raise ValueError(f"Use unique, flat title/version/updated/effective/status fields: {source}: {line}")
            value = value.strip()
            if value.startswith('"'):
                value = json.loads(value)
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1].replace("''", "'")
            elif value in ("", "null", "~"):
                value = None
            if value is not None and not isinstance(value, str):
                raise ValueError(f"Metadata must contain text: {source}: {key}")
            metadata[key] = value
        text = "\n".join(lines[end+1:])
    parser = MarkdownIt("commonmark", {"html": False})
    tokens = parser.parse(text)
    title = metadata.get("title")
    # A normal '# Article title' is enough for draft articles, without front matter.
    if tokens and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
        heading = tokens[1].content
        if title and title != heading:
            raise ValueError(f"Front-matter title differs from the first heading: {source}")
        title = heading
        tokens = tokens[3:]
    if not title:
        raise ValueError(f"Add a '# Title' or title metadata: {source}")

    def prepare(items):
        for token in items:
            if token.type == "heading_open" and token.tag == "h1":
                raise ValueError(f"Use one document title, then ## and ### headings: {source}")
            if token.type == "link_open":
                href = token.attrGet("href")
                url = urlsplit(href)
                if not url.scheme and not url.netloc and url.path.endswith(".md"):
                    target = (source.parent / unquote(url.path)).resolve()
                    try:
                        parts = target.relative_to(content_root.resolve()).parts
                    except ValueError:
                        raise ValueError(f"Markdown link leaves content directory: {source}: {href}")
                    if len(parts) != 3 or not target.is_file():
                        raise ValueError(f"Missing Markdown document: {source}: {href}")
                    path = base + "/" + "/".join(quote(p, safe="-") for p in (*parts[:2], target.stem)) + "/"
                    token.attrSet("href", urlunsplit(("", "", path, url.query, url.fragment)))
            if token.children:
                prepare(token.children)

    prepare(tokens)
    sections, introduction, current = [], [], None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == "heading_open" and token.tag == "h2" and token.level == 0:
            heading = tokens[index+1].content
            explicit = re.search(r"\s+\{#([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\}\s*$", heading)
            section_id = explicit.group(1) if explicit else f"section-{len(sections)+1}"
            heading = heading[:explicit.start()].rstrip() if explicit else heading
            current = {"id":section_id, "title":heading, "tokens":[]}
            sections.append(current)
            index += 3
        else:
            (current["tokens"] if current else introduction).append(token)
            index += 1
    for section in sections:
        section["html"] = parser.renderer.render(section.pop("tokens"), parser.options, {})
    return {"title":title, "version":metadata.get("version") or "1.0", "updated":metadata.get("updated"),
            "effective":metadata.get("effective"), "status":metadata.get("status") or "draft", "sections":sections,
            "introduction_html":parser.renderer.render(introduction, parser.options, {})}
