# The Git Mistakes Rescue Handbook

*A beginner manual for recovering from git panic.*

You know the feeling. You ran one git command, something unpredictable
happened, your stomach dropped, and now you're scrolling frantic search
results with one hand hovering over the power button. This handbook is
for exactly that moment — and for the moment you'd like to never have
again.

Git is designed so that your work is almost never actually lost. The hard
part is knowing which handful of commands bring it back. That's all this
book teaches: **plain-English, step-by-step rescues for the most common
git panics**, organized around a decision table that starts with the
honest question — *"what did you just do?"*

Covers: uncommitted work · wrong branch · bad merges · staged-changes
panic · detached HEAD · force-push fears · "my commit vanished."

Built as a **distilled companion** to a broader GitHub handbook (see
*[github-for-everyone-handbook](../github-for-everyone-handbook/)* style
projects): that one teaches the ecosystem end to end; this one is the
calm rescue kit you keep open in a crisis.

## What's inside

```
docs/    The handbook in Markdown
  index.md      The decision table: "what did you just do?"
  01-alpha...   Each panic chapter: uncommitted work, wrong branch,
                bad merge, staged changes, detached HEAD, force-push,
                vanished commits, universal safety net
  09-pocket...  Pocket card: every rescue command on one page
site/    Static HTML version of the same handbook (plain, no JavaScript)
tools/   build_site.py — regenerates site/ from docs/ using only Python's
         standard library. No installs, no frameworks.
```

## Read it

- Directly: open `docs/index.md` and start with the **decision table**.
- As a site: open `site/index.html`, or serve it locally:

```bash
python3 tools/build_site.py   # rebuild site/ from docs/ (optional; prebuilt copy included)
python3 -m http.server 8000 --directory site
# then visit http://localhost:8000
```

Both options work offline, with no account, and looking at nothing but
your own files. That's on purpose — this is a panic handbook, and the
last thing you need mid-crisis is a dependency.

## The five-second philosophy

1. Almost nothing in git destroys your work.
2. `git status`, `git branch backup-*`, and `git reflog` are the three
   safe-to-always-run moves.
3. Never run anything with `--force` while panicked.
4. Commits are cheap bookmarks, not publications. Commit ugly, early.

The full decision table lives in
[docs/index.md](docs/index.md) (or [site/index.html](site/index.html)).

## Who this is for

Anyone using git — nurses learning to code, small-business owners,
students, self-taught authors, developers with twenty years of typing who
still feel that specific git dread. It's written in the plain, warm,
never-condescending style of Asdale Dynamics projects like
*The Massive AI Manual*.

## Run / verify

```bash
python3 tools/build_site.py          # regenerate site/ from docs/
python3 tools/check_site.py          # verify links + HTML structure
```

`check_site.py` confirms every internal link in `site/` and `docs/`
resolves to a real file. No test framework required.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC. Made by Dylan Asdale's
Asdale Dynamics, LLC — beginner-friendly AI education, books, and
practical tools explained like a friend would.
