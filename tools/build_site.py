#!/usr/bin/env python3
"""Build the static HTML site/ from docs/.

Standard library only -- no pip installs, no frameworks.
Usage:  python3 tools/build_site.py
Output: site/index.html and one .html per docs/*.md page.
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

TITLE = "The Git Mistakes Rescue Handbook"
DESCRIPTION = (
    "A beginner manual for recovering from git panic: uncommitted work, "
    "wrong branch, bad merge, staged changes, detached HEAD, force-push "
    "fears, vanished commits. Plain English, step by step."
)

inline_re = re.compile(
    r"(`[^`]+`)"                       # 1: code span
    r"|(\*\*\*[^*\n]+\*\*\*)"          # 2: bold+italic
    r"|(\*\*[^*\n]+\*\*)"              # 3: bold
    r"|(\*[^*\n]+\*)"                  # 4: italic
    r"|(\[[^\]]+\]\([^)\s]+\))"        # 5: link
)


def render_inline(text: str) -> str:
    """Escape HTML, then apply code/bold/italic/link spans."""
    parts = []
    pos = 0
    for m in inline_re.finditer(text):
        parts.append(html.escape(text[pos:m.start()]))
        token = m.group(0)
        if m.group(1):  # code span
            parts.append(f"<code>{token[1:-1]}</code>")
        elif m.group(2):
            parts.append(f"<strong><em>{token[3:-3]}</em></strong>")
        elif m.group(3):
            parts.append(f"<strong>{token[2:-2]}</strong>")
        elif m.group(4):
            parts.append(f"<em>{token[1:-1]}</em>")
        elif m.group(5):
            label = token[1:token.index("]")]
            href = token[token.index("(") + 1:token.rindex(")")]
            if href.endswith(".md"):  # internal md links become html links
                href = href[:-3] + ".html"
            cls = " class=\"ext\"" if href.startswith(("http://", "https://")) else ""
            rel = ' rel="noopener"' if cls else ""
            parts.append(f"<a href=\"{html.escape(href, quote=True)}\"{cls}{rel}>{html.escape(label)}</a>")
        pos = m.end()
    parts.append(html.escape(text[pos:]))
    return "".join(parts)


def slugify(heading: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return slug


def render_blocks(md_text: str) -> str:
    out = []
    lines = md_text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        # fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            code = html.escape("\n".join(buf))
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{code}\n</code></pre>")
            continue
        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|?\s*$", lines[i + 1]):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                cells += [""] * (len(header) - len(cells))
                rows.append(cells[: len(header)])
                i += 1
            out.append("<table>")
            out.append("<thead><tr>" + "".join(f"<th>{render_inline(c)}</th>" for c in header) + "</tr></thead>")
            out.append("<tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            slug = slugify(text) if level <= 3 else ""
            out.append(f'<h{level} id="{slug}">{render_inline(text)}</h{level}>')
            i += 1
            continue
        # horizontal rule
        if re.match(r"^\s*---\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{render_blocks(chr(10).join(buf))}</blockquote>")
            continue
        # unordered list
        if re.match(r"^\s*[-*]\s+", line):
            buf = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i]).strip()
                if re.match(r"^\[[ x]\]\s", item):  # checkbox list
                    checked = item.startswith("[x]")
                    item = re.sub(r"^\[[ x]\]\s+", "", item)
                    box = "checked" if checked else ""
                    buf.append(f'<li class="check"><input type="checkbox" disabled {box}> {render_inline(item)}</li>')
                else:
                    buf.append(f"<li>{render_inline(item)}</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
            continue
        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            buf = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip()
                buf.append(f"<li>{render_inline(item)}</li>")
                i += 1
            out.append("<ol>" + "".join(buf) + "</ol>")
            continue
        # paragraph
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|\s*[-*]\s|\s*\d+\.\s|\||>)", lines[i]) and not re.match(r"^\s*---\s*$", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{render_inline(' '.join(s.strip() for s in buf))}</p>")
    return "\n".join(out)


CSS = """\
:root { --ink:#1f2430; --paper:#fdfdfb; --accent:#3b6e64; --card:#eef4f0; --line:#d9e2dd; }
* { box-sizing:border-box; }
body { margin:0; font-family:Georgia,'Times New Roman',serif; color:var(--ink); background:var(--paper); line-height:1.65; font-size:17px; }
header.site, footer.site { max-width:46rem; margin:0 auto; padding:1.5rem 1.25rem; }
header.site h1 { margin:0; font-size:1.9rem; color:var(--accent); }
header.site p { margin:.3rem 0 0; color:#576057; }
main { max-width:46rem; margin:0 auto; padding:0 1.25rem 3rem; }
h1,h2,h3,h4 { line-height:1.25; }
h2 { color:var(--accent); margin-top:2.2rem; border-bottom:2px solid var(--line); padding-bottom:.3rem; }
h3 { margin-top:1.6rem; }
a { color:var(--accent); }
a.ext::after { content:"\\2197"; font-size:.8em; }
pre { background:#2b313a; color:#e8ecf1; padding:1rem 1.2rem; border-radius:8px; overflow-x:auto; font-size:.88rem; line-height:1.5; }
code { font-family:ui-monospace,'SF Mono',Consolas,monospace; }
p code, li code, td code, th code, h2 code { background:var(--card); border:1px solid var(--line); border-radius:4px; padding:.08em .35em; font-size:.85em; }
pre code { background:none; border:none; padding:0; color:inherit; font-size:1em; }
table { border-collapse:collapse; width:100%; font-size:.92rem; margin:1.2rem 0; }
th,td { border:1px solid var(--line); padding:.5rem .7rem; text-align:left; vertical-align:top; }
th { background:var(--card); }
blockquote { border-left:4px solid var(--accent); background:var(--card); margin:1.2rem 0; padding:.6rem 1rem; border-radius:0 8px 8px 0; }
blockquote p { margin:.3rem 0; }
input[type=checkbox] { accent-color:var(--accent); }
nav.pagenav { display:flex; justify-content:space-between; gap:1rem; border-top:2px solid var(--line); margin-top:2.5rem; padding-top:1rem; font-size:.95rem; }
footer.site { color:#576057; font-size:.85rem; border-top:1px solid var(--line); margin-top:2rem; }
footer.site a { color:inherit; }
nav.toc { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:1rem 1.4rem; margin:1.4rem 0; font-size:.95rem; }
nav.toc ol { margin:.4rem 0; padding-left:1.2rem; }
"""


def page_shell(title: str, body: str, nav_html: str, footer_text: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<style>
{CSS}
</style>
</head>
<body>
<header class="site">
<h1><a href="index.html" style="text-decoration:none;color:inherit">The Git Mistakes Rescue Handbook</a></h1>
<p>Recover from git panic. Plain English, step by step, never condescending.</p>
</header>
<main>
{body}
<nav class="pagenav">{nav_html}</nav>
</main>
<footer class="site">
<p>{footer_text}</p>
</footer>
</body>
</html>
"""


def collect_pages():
    pages = sorted(DOCS.glob("*.md"))
    # decision table (index) comes first, then chapters in filename order
    pages.sort(key=lambda p: (p.stem != "index", p.name))
    result = []
    for p in pages:
        html_name = "index.html" if p.stem == "index" else p.stem + ".html"
        result.append((p, html_name))
    return result


def nav_for(pos, titles):
    prev_html = '<span></span>'
    if pos > 0:
        prev_name = "index.html" if pages_list[pos - 1][0].stem == "index" else f"{pages_list[pos-1][0].stem}.html"
        prev_html = f'<a href="{prev_name}">&larr; {html.escape(titles[pages_list[pos-1][0].stem])}</a>'
    nxt_html = '<span></span>'
    if pos + 1 < len(pages_list):
        nxt_name = "index.html" if pages_list[pos + 1][0].stem == "index" else f"{pages_list[pos+1][0].stem}.html"
        nxt_html = f'<a href="{nxt_name}">{html.escape(titles[pages_list[pos+1][0].stem])} &rarr;</a>'
    return prev_html, nxt_html


pages_list = collect_pages()


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    # first pass: titles for nav labels
    titles = {}
    bodies = {}
    for path, html_name in pages_list:
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^#\s+(.+)$", text, re.M)
        titles[path.stem] = m.group(1).strip() if m else path.stem
        bodies[path.stem] = render_blocks(text)

    n = len(pages_list)

    for idx, (path, html_name) in enumerate(pages_list):
        pos = idx
        body = bodies[path.stem]
        if path.stem == "index":
            toc_items = "".join(
                f'<li><a href="{p.stem}.html">{html.escape(titles[p.stem])}</a></li>'
                for p, _ in pages_list[1:]
            )
            body = body + f'<nav class="toc"><strong>Chapters</strong><ol>{toc_items}</ol></nav>'
        prev_html, nxt_html = nav_for(pos, titles)
        footer_text = (
            "The Git Mistakes Rescue Handbook &middot; "
            "Copyright (c) 2026 Asdale Dynamics, LLC &middot; MIT License &middot; "
            "Friendly git education; not affiliated with the git project."
        )
        SITE.joinpath(html_name).write_text(
            page_shell(titles[path.stem], body, prev_html + nxt_html, footer_text),
            encoding="utf-8",
        )
        print(f"built {html_name}")

    print(f"done: {len(pages_list)} pages")


if __name__ == "__main__":
    main()
