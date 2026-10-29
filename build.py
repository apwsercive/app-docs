"""Build a portable multi-app Markdown/JSON document site for GitHub Pages."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote
from markdown_content import read_markdown

ROOT = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def segment(value):
    if not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", value):
        raise ValueError(f"Unsafe URL segment: {value}")
    return value


def build(base_path="", output=None, release=False):
    config = load(ROOT / "site.json")
    out = Path(output).resolve() if output else ROOT / "dist"
    if out == ROOT or ROOT in out.parents and out != ROOT / "dist":
        raise ValueError("Use dist or an external output directory")
    if base_path and not re.fullmatch(r"/?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?", base_path):
        raise ValueError("Base path must be a URL path, for example /app-docs")
    if any(part in (".", "..") for part in base_path.split("/")):
        raise ValueError("Base path cannot contain dot segments")
    base = "/" + base_path.strip("/") if base_path.strip("/") else ""
    locales = config["locales"]
    publisher = config["publisher"]
    if publisher.get("email") and not re.fullmatch(r"[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+", publisher["email"]):
        raise ValueError("Invalid publisher email")
    docs = {}
    for app_id, app in config["apps"].items():
        segment(app_id)
        discovered = sorted({p.stem for locale in app["names"]
                             for p in (ROOT / "content" / app_id / segment(locale)).glob("*.md")})
        app["documents"] = list(dict.fromkeys(app.get("documents", []) + discovered))
        for locale in app["names"]:
            segment(locale)
            if locale not in locales:
                raise ValueError(f"Missing UI translations: {locale}")
            for kind in app["documents"]:
                segment(kind)
                folder = ROOT / "content" / app_id / locale
                markdown, legacy = folder / f"{kind}.md", folder / f"{kind}.json"
                if markdown.exists() and legacy.exists():
                    raise ValueError(f"Keep one Markdown or JSON source per document: {markdown}")
                source = markdown if markdown.exists() else legacy
                if source.exists():
                    doc = read_markdown(source, ROOT / "content", base) if source.suffix == ".md" else load(source)
                    if doc["updated"]:
                        date.fromisoformat(doc["updated"])
                    if doc["effective"]:
                        date.fromisoformat(doc["effective"])
                    if doc["status"] not in ("draft", "published"):
                        raise ValueError(f"Invalid status: {source}")
                    if doc["status"] == "published" or release:
                        if not all((publisher.get("name"), publisher.get("email"), doc["effective"], doc["updated"])) or doc["status"] != "published":
                            raise ValueError(f"Release needs operator, email, effective date and published status: {source}")
                    ids = [s["id"] for s in doc["sections"]]
                    if len(ids) != len(set(ids)) or "contact" in ids or "main" in ids:
                        raise ValueError(f"Duplicate or reserved section IDs: {source}")
                    for section in doc["sections"]:
                        segment(section["id"])
                    docs[app_id, locale, kind] = doc
    if not docs:
        raise ValueError("No documents found")
    # Validate all sources before writing output. Never clear an arbitrary directory.
    out.mkdir(parents=True, exist_ok=True)
    for old in out.rglob("*"):
        if old.is_file():
            raise ValueError("Output must be empty; remove the generated dist directory before rebuilding")

    def url(path=""):
        return escape(base + "/" + path, quote=True)

    def link(path, text, attrs=""):
        return f'<a href="{url(path)}" {attrs}>{escape(text)}</a>'

    def paragraph(text):
        return f"<p>{escape(text)}</p>"

    def write(path, title, locale, body, nav="", alternates=None):
        t = locales[locale]
        alternate_tags = "".join(f'<link rel="alternate" hreflang="{escape(lang)}" href="{url(p)}">' for lang, p in (alternates or {}).items())
        robots = '<meta name="robots" content="noindex, nofollow">' if any(d["status"] == "draft" for d in docs.values()) else ""
        html = f'''<!doctype html>
<html lang="{escape(locale)}" dir="{escape(t['dir'])}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">{robots}
<meta name="description" content="{escape(t['intro'])}">
<title>{escape(title)} · {escape(t['home'])}</title>
<link rel="stylesheet" href="{url('assets/style.css')}">{alternate_tags}</head>
<body><a class="skip" href="#main">{escape(t['skip'])}</a>
<header><nav aria-label="{escape(t['home'])}">{link(locale+'/', t['home'], 'class="brand"')}{nav}</nav></header>
<main id="main" tabindex="-1">{body}</main>
<footer><p>{escape(t['operator'])}: {escape(publisher.get('name') or t['pending'])}</p>
<nav aria-label="External policies"><a href="https://www.apple.com/legal/privacy/">Apple Privacy</a>
<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy</a>
<a href="https://support.apple.com/118428">Apple Subscriptions</a></nav></footer></body></html>'''
        dest = out / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

    def language_nav(paths, current):
        return '<div class="languages">' + "".join(link(p, locales[lang]["label"], f'lang="{lang}" hreflang="{lang}"' + (' aria-current="page"' if lang == current else "")) for lang, p in paths.items()) + "</div>"

    default = next(iter(locales))
    chooser = f'<h1>{escape(config["title"])}</h1>'
    chooser += '<ul class="list">' + "".join(f'<li>{link(lang+"/", t["label"], f"lang={lang}")}</li>' for lang, t in locales.items()) + '</ul>'
    write("index.html", config["title"], default, chooser)
    for locale, t in locales.items():
        body = f'<h1>{escape(t["home"])}</h1>' + paragraph(t["intro"]) + '<ul class="list">'
        for app_id, app in config["apps"].items():
            if any(a == app_id and l == locale for a, l, _ in docs):
                body += f'<li>{link(f"{app_id}/{locale}/", app["names"][locale])}</li>'
        body += '</ul>'
        paths = {lang: f"{lang}/" for lang in locales}
        write(f"{locale}/index.html", t["home"], locale, body, language_nav(paths, locale), paths)

    for app_id, app in config["apps"].items():
        available = {lang: f"{app_id}/{lang}/" for lang in app["names"] if any(a == app_id and l == lang for a, l, _ in docs)}
        chooser = f'<h1>{escape(next(iter(app["names"].values())))}</h1><ul class="list">'
        chooser += "".join(f'<li>{link(path, locales[lang]["label"], f"lang={lang}")}</li>' for lang, path in available.items()) + '</ul>'
        write(f"{app_id}/index.html", next(iter(app["names"].values())), default, chooser)
        for locale, app_path in available.items():
            t = locales[locale]
            body = f'<h1>{escape(app["names"][locale])}</h1><ul class="list">'
            body += "".join(f'<li>{link(f"{app_path}{kind}/", docs[app_id,locale,kind]["title"])}</li>' for kind in app["documents"] if (app_id,locale,kind) in docs) + '</ul>'
            write(f"{app_path}index.html", app["names"][locale], locale, body, language_nav(available, locale), available)

    for (app_id, locale, kind), doc in docs.items():
        t = locales[locale]
        app = config["apps"][app_id]
        paths = {lang: f"{app_id}/{lang}/{kind}/" for lang in app["names"] if (app_id,lang,kind) in docs}
        nav = language_nav(paths, locale)
        body = '<nav class="breadcrumb" aria-label="Breadcrumb">' + link(f"{app_id}/{locale}/", app["names"][locale]) + '</nav>'
        body += f'<h1>{escape(doc["title"])}</h1><dl class="metadata">'
        for label, value in ((t["updated"],doc["updated"] or t["pending"]),(t["effective"],doc["effective"] or t["pending"]),(t["version"],doc["version"])):
            body += f'<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>'
        body += '</dl>'
        if doc["status"] == "draft":
            body += f'<aside class="notice">{escape(t["draft"])}</aside>'
        body += doc.get("introduction_html", "")
        sections = doc["sections"] + [{"id":"contact", "title":t["contact"], "paragraphs":[]}]
        body += f'<nav class="contents" aria-label="{escape(t["contents"])}"><h2>{escape(t["contents"])}</h2><ul>'
        body += "".join(f'<li><a href="#{s["id"]}">{escape(s["title"])}</a></li>' for s in sections) + '</ul></nav><article>'
        for section in sections:
            body += f'<section id="{section["id"]}"><h2>{escape(section["title"])}</h2>'
            body += section.get("html", "") + "".join(paragraph(p) for p in section.get("paragraphs", []))
            if section["id"] == "contact":
                body += paragraph(t["operator"] + ": " + (publisher.get("name") or t["pending"]))
                if publisher.get("email"):
                    email = publisher["email"]
                    body += f'<p><a href="mailto:{quote(email, safe="@.+")}">{escape(email)}</a></p>'
                else:
                    body += paragraph(t["pending"])
            body += '</section>'
        body += '</article><nav class="related" aria-label="'+escape(t["documents"])+'">'
        body += "".join(link(f"{app_id}/{locale}/{k}/", docs[app_id,locale,k]["title"], 'aria-current="page"' if k == kind else "") for k in app["documents"] if (app_id,locale,k) in docs) + '</nav>'
        write(f"{app_id}/{locale}/{kind}/index.html", doc["title"] + " · " + app["names"][locale], locale, body, nav, paths)
    (out / "assets").mkdir()
    shutil.copyfile(ROOT / "assets/style.css", out / "assets/style.css")
    (out / ".nojekyll").touch()
    (out / "build-info.json").write_text(json.dumps({"base_path":base,"documents":len(docs)},indent=2)+"\n")
    print(f"Built {len(docs)} documents in {out} (base path: {base or '/'})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-path", default="")
    parser.add_argument("--output")
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    build(args.base_path, args.output, args.release)
