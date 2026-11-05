# Chapter 3 — Bad Merge Panic

*"I ran `git merge` and now there are conflict markers everywhere / the
build is broken / I don't understand what happened."*

Merges are where most beginner terror lives, so let's demystify. A merge
just weaves two lines of history into one commit. It does not delete
either line. Which means: every bad merge can be undone, usually with one
command, depending on how far the merge got.

## Stage 0: Conflicts are open and scaring you

If the merge has *paused* with conflict messages and your files now
contain blocks like:

```
<<<<<<< HEAD
ours version
=======
their version
>>>>>>> other-branch
```

**Do this first:** you can simply call the whole thing off:

```bash
git merge --abort
```

That is the official "forget this merge, put everything back how it was
before I started" button. Your branch returns to exactly its previous
state. Conflicts markers vanish. You lose nothing except the merge (which
you were going to cancel anyway).

Why conflicts happen, briefly: both branches changed the *same lines* and
git refuses to guess which you meant. It's not an error — it's a
politeness. Next time, you edit those `<<<<<<` files by hand (keeping the
version you want, deleting the markers) and `git add` them. But today you
don't have to.

## Stage 1: The merge already completed, before you noticed

If the merge finished and made a merge commit (git printed something like
"Merge made by the 'ort' strategy") and *you haven't pushed it*:

```bash
git reset --hard ORIG_HEAD
```

**What this actually does:** `ORIG_HEAD` is a bookmark git saved pointing
to where you were *before* the last big move (a merge, a rebase, a reset).
Resetting to it rewinds your branch to that exact spot. The merged content
stops being part of your branch.

Before running it, glance with `git log --oneline --graph -10` that
`ORIG_HEAD` is where you expect; print it with `git rev-parse ORIG_HEAD`
if you want the raw id. And keep your standing rule: `git branch
backup-before-merge` first, always.

```bash
git branch backup-before-undo    # bookmark. always.
git log --oneline --graph -10    # look around. always.
git reset --hard ORIG_HEAD       # now undo, calmly.
```

If `ORIG_HEAD` isn't what you want (you've done several operations since),
find your "before" moment in `git reflog` instead — Chapter 7 explains it
line by line.

## Stage 2: The bad merge already got pushed

Do **not** reset and force-push a shared branch before reading Chapter 6.
The safe, boring, team-approved undo is a *revert*:

```bash
git revert -m 1 the-merge-commit-id
```

`revert` doesn't rewrite history; it adds a new commit that undoes the
merge, like an "undo entry" in the diary. `-m 1` tells git you want to
keep your branch's side (the first parent) and undo the other side. Once
it's pushed, everyone just gets a normal commit. Nobody's day is ruined.

One classic gotcha: re-merging the same branch later will *not* redo the
content (git remembers it was merged). When that bites you, it's another
merge, not a crisis — and now you know to look at Chapter 7.

## Why merges feel scarier than they are

Uncommitted work in your files does not vanish during a merge conflict —
it just sits there until you abort or finish. And even after the most
chaotic conflicted merge, the *commits themselves* on both branches are
untouched. Merges weave; they don't unravel. Every scary merge outcome
above lands on either `merge --abort`, `reset --hard ORIG_HEAD`, or
`revert -m 1`. That's the whole spellbook.

[Back to the decision table](index.md)
