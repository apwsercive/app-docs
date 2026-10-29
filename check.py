"""Integration checks for URLs, translations, release metadata, and expansion."""
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.lang = [], set(), None
        self.headings, self.viewport, self.main = 0, False, False
        self.alternates = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, a["id"]
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
            assert a.get("dir") in ("ltr", "rtl")
        if tag == "h1":
            self.headings += 1
        if tag == "main":
            self.main = True
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
            assert "user-scalable=no" not in a["content"]
        assert tag not in ("script", "iframe", "form"), tag
        if tag in ("a", "link"):
            self.links.append(a.get("href", ""))
            if a.get("rel") == "alternate":
                self.alternates[a["hreflang"]] = a["href"]


def check(out, base):
    pages = {}
    for path in out.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        assert page.lang and page.viewport and page.headings == 1 and page.main, path
        pages[path] = page
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme:
                assert url.scheme in ("https", "mailto"), href
                continue
            if not url.path:
                target = path
            else:
                assert url.path.startswith(base + "/"), (path, href)
                target = out / unquote(url.path[len(base)+1:])
                if url.path.endswith("/"):
                    target /= "index.html"
                assert target.exists(), (path, href)
            if url.fragment:
                assert target in pages and url.fragment in pages[target].ids, (path, href)
        for lang, href in page.alternates.items():
            target = out / href[len(base)+1:] / "index.html"
            assert pages[target].lang == lang
    assert (out / ".nojekyll").exists()
    return len(pages)


def run():
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "site"
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("dist", "__pycache__", ".git"))
        spec = importlib.util.spec_from_file_location("site_build", work / "build.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        baseline_pages = None
        for label, base in (("root", ""), ("project", "/app-docs")):
            out = Path(tmp) / label
            module.build(base, out)
            page_count = check(out, base)
            if baseline_pages is None:
                baseline_pages = page_count
            assert page_count == baseline_pages
            en = (out / "kongming/en/privacy/index.html").read_text()
            assert f'{base}/kongming/zh-Hans/privacy/' in en
            assert 'id="location"' in en and 'GitHub' in en
        try:
            module.build(output=Path(tmp)/"release-rejected", release=True)
        except ValueError as error:
            assert "Release needs" in str(error)
        else:
            raise AssertionError("Incomplete release was accepted")
        config = json.loads((work/"site.json").read_text())
        config["publisher"] = {"name":"Test operator", "email":"test@example.com"}
        config["locales"]["ar"] = dict(config["locales"]["en"], label="العربية", dir="rtl")
        config["apps"]["example-app"] = {"names":{"ar":"Example"}, "documents":["support"]}
        # Convert fixtures to legacy JSON to exercise backward compatibility too.
        for path in (work/"content").rglob("*.md"):
            doc = module.read_markdown(path, work/"content", "")
            for section in doc["sections"]:
                section["paragraphs"] = []
            path.with_suffix(".json").write_text(json.dumps(doc))
            path.unlink()
        source = json.loads((work/"content/kongming/en/privacy.json").read_text())
        source["title"] = "Support"
        target = work/"content/example-app/ar/support.json"
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(source))
        (work/"site.json").write_text(json.dumps(config))
        for path in (work/"content").rglob("*.json"):
            doc = json.loads(path.read_text())
            doc.update(status="published", effective="2026-10-29", updated="2026-10-29")
            path.write_text(json.dumps(doc))
        out = Path(tmp)/"expanded"
        module.build("/documents", out, release=True)
        assert check(out, "/documents") == baseline_pages + 4
        ar = (out/"example-app/ar/support/index.html").read_text()
        assert 'dir="rtl"' in ar
        assert '/example-app/en/support/' not in ar
        assert 'noindex' not in ar
        # A Markdown article needs only a title; no JSON registration is required.
        article = work/"content/kongming/en/guide.md"
        article.write_text('# Getting started\n\nIntroduction with **bold** and `code`.\n\n## Choices {#choices}\n\n- First\n- Second\n\n> A note\n\n[中文隐私](../zh-Hans/privacy.md#location)\n\n<script>alert(1)</script>\n\n[unsafe](javascript:alert(1))\n\n```text\n## Not a heading\n```\n')
        # Use Markdown for the linked target as a real author would.
        target = work/'content/kongming/zh-Hans/privacy.md'
        target.write_text('# 隐私协议\n\n## 水印相机与位置 {#location}\n\n内容\n')
        target.with_suffix('.json').unlink()
        out = Path(tmp)/"markdown-article"
        module.build('/app-docs', out)
        check(out, '/app-docs')
        html = (out/'kongming/en/guide/index.html').read_text()
        assert '<strong>bold</strong>' in html and '<code>code</code>' in html
        assert '<ul>' in html and '<blockquote>' in html and '<pre><code' in html
        assert 'id="choices"' in html and 'Not a heading</h2>' not in html
        assert '&lt;script&gt;' in html and '<script>' not in html
        assert 'href="javascript:' not in html
        assert '/app-docs/kongming/zh-Hans/privacy/#location' in html
        assert '/app-docs/kongming/en/guide/' in (out/'kongming/en/index.html').read_text()
        assert '/kongming/zh-Hans/guide/' not in html
        # Never silently pick a stale JSON copy when both formats exist.
        article.with_suffix('.json').write_text('{}')
        try:
            module.build(output=Path(tmp)/'duplicate-format')
        except ValueError as error:
            assert 'Keep one Markdown or JSON' in str(error)
        else:
            raise AssertionError('Duplicate Markdown/JSON source accepted')
        print("Passed: Markdown policy migration, automatic article discovery, Markdown formatting and links, raw HTML escaping, legacy JSON, root/project URLs, anchors, release validation, additional app and RTL locale.")


if __name__ == "__main__":
    run()
