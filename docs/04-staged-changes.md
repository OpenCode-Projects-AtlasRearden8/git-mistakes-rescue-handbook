# Chapter 4 — Staged Changes Panic

*"I ran some command and now everything is green in `git status` and I
don't know what's about to happen if I commit."* (Or: *"I staged a file I
didn't mean to — is my secret going into the commit?"*)

First, untangle a vocabulary knot that confuses everyone:

- **Working directory**: the files as they are right now on your screen.
- **Staging area (the "index")**: the *photo tee you've posed for the next
  commit*. It's a place, and staging a file only puts a copy of it in that
  place.
- **Commit**: the photo actually taken.

**Staging commits nothing. Nothing leaves your machine at any stage.
Staging is purely "assembling" — it is the least dangerous thing in git.**

## Do this first

To unstage everything and go back to "I'm just editing files":

```bash
git restore --staged .
```

The dot means "all currently staged files." After this, `git status`
shows everything as "not staged for commit" again. Zero edits were lost —
your files never moved. All that happened is the *photo pose* got relaxed.

To unstage just one file:

```bash
git restore --staged path/to/file
```

(On very old git you'd see `git reset HEAD path/to/file` suggested — same
effect, older phrasing.)

## "I staged everything by accident"

Probably `git add -A` or `git add .` — both are fine tools, but they
sweep. Either unstage what you don't want (above), or just *commit in
stages*: commit what's there with a clear message, keep working, commit
again later. Two small tidy commits beat one anxious staging session.

## "I staged something I really don't want recorded — a secret-looking file"

This is the one staging panic that deserves speed, and the answer is:
staged is your *friend* here, because a file that never gets committed
never enters history. So:

1. Unstage it: `git restore --staged the-file`
2. Add it to `.gitignore` so it never gets swept up again:

```bash
echo ".env" >> .gitignore
git add .gitignore
```

3. If it was already committed *before* today's panic, the file is sitting
   in git's history. That's Chapter 8 territory — see the "exposed secret"
   note there. The short version: treat the exposed value as burned,
   replace/rotate it, and then clean history calmly.

## What staging does NOT do

- It does not push anywhere. Pushing is a separate act entirely.
- It does not delete your working copy. Nothing about staging removes,
  moves, or rewrites file contents.
- It does not follow you into `stash` or confuse merges. It's just
  preparation.

## A habit that dissolves this panic forever

Use `git add path/to/thing` for *specific* files when you want to be
deliberate, and `git add -A` when you truly mean "all of it." That's the
entire nuance. If you ever feel your pulse rise in `git status`, remember
the peace treaty: `git restore --staged .` resets the pose, never the files.

[Back to the decision table](index.md)
