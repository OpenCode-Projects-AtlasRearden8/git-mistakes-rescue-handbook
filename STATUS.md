# STATUS.md — The Git Mistakes Rescue Handbook

Last updated: 2026-11-05

## What was built

A beginner-friendly panic-recovery manual for git, written in the plain,
warm style of Asdale Dynamics (LLC) education projects — the rescue-kit
companion to a broader GitHub handbook (distinct from
github-for-everyone-handbook, which teaches the ecosystem end to end; this
covers only the "I broke it" moments).

Contents:

- **docs/** — 10 Markdown pages:
  - `index.md` — the decision table: "what did you just do?" with 9
    situational rows, each linking to a full walkthrough
  - `01` uncommitted work, `02` wrong branch, `03` bad merge,
    `04` staged-changes panic, `05` detached HEAD, `06` force-push fears,
    `07` "my commit vanished" (reflog rescue), `08` universal safety net,
    `09` pocket card (every rescue command on one page)
- **site/** — a static HTML rendering of the same handbook (styled, no
  JavaScript, workable offline). Prebuilt; regenerate with `tools/build_site.py`.
- **tools/build_site.py** — stdlib-only Python generator (no pip installs,
  no frameworks): converts docs/*.md to styled site/*.html with nav,
  tables, code blocks, prev/next links.
- **tools/check_site.py** — stdlib-only verifier: checks every internal
  link in docs/ and site/, anchor fragments, table rendering, HTML
  structure, and scans for secret-looking strings.
- **README.md** (credits Asdale Dynamics, LLC), **LICENSE** (MIT,
  `Copyright (c) 2026 Asdale Dynamics, LLC`).

Style notes held throughout: plain English, "do this first" per chapter,
every scary command explained before use, no secrets/personal data in any
file, no force-running of dangerous examples without bookmarks first.

## How to run it

```bash
# build the HTML site from docs/ (optional; site/ is prebuilt)
python3 tools/build_site.py

# verify links + structure + no secret-like strings
python3 tools/check_site.py

# serve the site locally (localhost only, nothing is published)
python3 -m http.server 8000 --directory site
# visit http://localhost:8000
```

Or just read `docs/index.md` directly — the Markdown is the source of truth.

## Verification results (2026-11-05)

- `python3 tools/build_site.py` — builds 10/10 pages cleanly. PASS.
- `python3 tools/check_site.py` — "PASS: all links resolve, HTML structure
  OK, no secret-like strings." 10 markdown pages, 10 HTML pages checked.
- Local serve test: `python3 -m http.server` + curl returned HTTP 200 for
  `index.html` and chapter pages.
- Rescue examples tested hands-on in a disposable sandbox repo
  (`/tmp/opencode/gitpanic*`, git 2.47.3):
  - Ch1: `git stash` / `git stash pop` round-trip OK; `git restore`
    undeletes an uncommitted-deletion OK
  - Ch2: commit-to-wrong-branch surgery (bookmark + `branch fix-here` +
    `reset --hard`) keeps commits reachable OK
  - Ch3: conflict open + `git merge --abort` OK; completed merge undone
    via `git reset --hard ORIG_HEAD` OK; pushed-merge undo via
    `git revert --no-edit -m 1 <merge>` OK
  - Ch4: `git add` stages OK; `git restore --staged .` unstages OK
  - Ch5: detach at a commit, `git status` shows detached, `git switch -`
    returns OK; `git switch -c` rescues OK
  - Ch7: commit hidden by `git reset`, found in `git reflog`, rescued via
    `git branch rescue <id>` OK
- No secrets/API keys/personal data: verifier pattern-scan across all
  .md/.html/.py files. PASS.
- Committed locally as the existing git identity (no push, no remote).

## Known gaps

- The Markdown-to-HTML converter in `build_site.py` is intentionally
  minimal (headings, paragraphs, fenced code, tables, lists, quotes,
  inline code/bold/italic/links). Nested lists and inline HTML inside
  Markdown would not render — none are currently used, but adding them
  requires converter work.
- Chapter 6 intentionally explains remote-branch behavior generically;
  exact behavior of specific hosting services' web restores/reflogs is
  not covered (marked as such in the chapter).
- The site is a single flat directory with inline CSS (no pages > ~100px
  nav depth); adding pages means zero config, but featured links/theming
  are not built.
- Chapter 8's secret-handling section is deliberately brief — full
  history-surgery (`git filter-repo`) walkthroughs are out of scope for
  this handbook; it points to rotating the exposed value instead, which
  is the security-critical part.
- No automated tests beyond `tools/check_site.py` (as specified: no test
  framework required).
