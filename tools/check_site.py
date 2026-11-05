#!/usr/bin/env python3
"""Verify the handbook: markdown links, HTML links, HTML structure,
and absence of secret-looking strings. Stdlib only.

Usage: python3 tools/check_site.py
Exits non-zero on any failure.
"""

import html.parser
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

errors = []
warnings = []


def check_md_links():
    for md in DOCS.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\[[^\]]+\]\(([^)\s]+)\)", text):
            href = m.group(1)
            if href.startswith(("http://", "https://")):
                continue
            target = md.parent / href
            if not target.exists():
                errors.append(f"md link broken: {md.name} -> {href}")


class LinkParser(html.parser.HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.links = []
        self.ids = set()
        self.in_body = False
        self.stack = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append((d["href"], self.getpos()[0]))
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "body":
            self.in_body = True
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "table", "pre", "blockquote", "tr", "ul", "ol"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()


VOID_OK = {"input"}


def check_html():
    pages = sorted(SITE.glob("*.html"))
    if not pages:
        errors.append("no HTML pages in site/")
        return
    for page in pages:
        text = page.read_text(encoding="utf-8")
        parser = LinkParser(page)
        parser.feed(text)
        # links resolve (strip fragment for file check)
        for href, line in parser.links:
            if href.startswith(("http://", "https://", "#")):
                continue
            target = page.parent / href.split("#")[0]
            if not target.exists():
                errors.append(f"html link broken: {page.name}:{line} -> {href}")
            elif "#" in href:
                frag = href.split("#", 1)[1]
                target_text = target.read_text(encoding="utf-8")
                if f'id="{frag}"' not in target_text:
                    errors.append(f"html fragment broken: {page.name}:{line} -> {href}")
        # internal fragments
        for href, line in parser.links:
            if href.startswith("#") and href != "#":
                frag = href[1:]
                if frag not in parser.ids:
                    errors.append(f"missing anchor: {page.name}:{line} -> {href}")
        # structural expectations
        for needle in ("<title>", "<main>", "</main>", "</html>"):
            if needle not in text:
                errors.append(f"missing {needle!r} in {page.name}")
        if "<h1" not in text:
            errors.append(f"missing <h1> in {page.name}")
        # markdown tables must have been rendered as <table>
        md_src = DOCS / (page.stem + ".md")
        if md_src.exists():
            md_text = md_src.read_text(encoding="utf-8")
            md_tables = len(re.findall(r"^\|.+\n\|[-: |]+\|", md_text, re.M))
            html_tables = text.count("<table>")
            if md_tables and html_tables != md_tables:
                errors.append(f"table count mismatch in {page.name}: md={md_tables} html={html_tables}")
        # unrendered markdown leftovers in HTML body (after </style>)
        body = text.split("</style>", 1)[1] if "</style>" in text else text
        for bad in ("| --- |", "](", "```"):
            if bad in body:
                errors.append(f"unrendered markdown in {page.name}: {bad!r}")


def check_secrets():
    patterns = [
        (r"ghp_[A-Za-z0-9]{10,}", "GitHub token shape"),
        (r"github_pat_[A-Za-z0-9_]{10,}", "GitHub PAT shape"),
        (r"AKIA[0-9A-Z]{16}", "AWS key id shape"),
        (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key"),
        (r"sk-[A-Za-z0-9]{20,}", "API key shape"),
        (r"(?i)password\s*[:=]\s*['\"][^'\"]{6,}", "hardcoded password"),
    ]
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.name in {"LICENSE"} or path.suffix not in {".md", ".html", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat, label in patterns:
            if re.search(pat, text):
                errors.append(f"secret-like string ({label}) in {path.relative_to(ROOT)}")


def main():
    if not DOCS.exists():
        errors.append("docs/ missing")
    check_md_links()
    check_html()
    check_secrets()

    n_md = len(list(DOCS.glob("*.md")))
    n_html = len(list(SITE.glob("*.html")))
    print(f"checked: {n_md} markdown pages, {n_html} html pages")
    if warnings:
        for w in warnings:
            print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("PASS: all links resolve, HTML structure OK, no secret-like strings")


if __name__ == "__main__":
    main()
