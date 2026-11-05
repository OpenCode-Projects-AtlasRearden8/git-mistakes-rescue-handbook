# Chapter 2 — Wrong Branch Panic

*"I was supposed to be on `main` but I've been typing away on `feature-x`
for an hour."* (Or the classic: *"I committed three times... on the wrong
branch."*)

Take a breath. Branches in git are just labels pointing at commits.
Labels can be moved. Work follows you. Almost nothing here is permanent.

## Case 1: You've been editing, but haven't committed yet

**Do this first:** nothing — your edits aren't attached to the branch at
all yet. Uncommitted changes live in your working directory; the branch is
just where the *next* commit will land.

Switch branches and bring the work with you:

```bash
git switch better-branch      # if the branch exists
git switch -c better-branch   # if it doesn't exist yet
```

Your uncommitted edits travel with you. If git refuses because the files
would clash with the other branch's contents, commit first (Chapter 1),
then switch, then sort it out.

## Case 2: You already committed to the wrong branch

Say you made commits A, B, C on `main` but they belong on a new branch.

**Do this first: make a bookmark before anything else.**

```bash
git branch backup-before-branch-surgery
```

Now the surgery. The plan:

1. Point the new (correct) branch at your current commits.
2. Move `main` back to where it should be.

```bash
git branch fix-here                      # 1: new branch at your commits
git reset --hard origin/main             # 2: drag main back to the real main
git switch fix-here                      # 3: stand on your rescued commits
```

That `reset --hard` line is the only scary-looking thing, and here's why
it's safe in this moment: you have *already* bookmarked your commits with
`fix-here` (and `backup-before-branch-surgery`). A commit that a branch
name points to cannot be destroyed by moving a *different* branch.

Notes:

- If there's no remote copy of `main` yet, instead use: `git branch tmp-main && git reset --hard tmp-main` — or simpler, note the commit id from `git log --oneline main` before you started and reset to it.
- If you already *pushed* the wrong commits to a shared `main`, stop and
  read Chapter 6 before rewriting anything. On a shared branch, prefer
  `git revert` (which adds an undoing commit) over `reset`.

## Case 3: You committed to an old feature branch instead of main

Same surgery, different dressing:

```bash
git switch main
git cherry-pick the-commit-id       # copy the commit onto main
git switch other-branch
git rebase --onto other-branch~1 other-branch main  # advanced; see below
```

In plain words, `git cherry-pick <id>` means "photocopy that one commit
onto the branch I'm standing on." Then remove it from the old branch later
(or just leave it there until the branch itself is cleaned up — an extra
copy is annoying, not dangerous).

If any of that flexibility is above your comfort level today, the
always-works fallback is:

```bash
git switch main
git merge other-branch          # bring the work over the ordinary way
```

Then continue on main. Not elegant; entirely acceptable.

## The safety net recap

Before *any* branch surgery:

```bash
git branch backup-just-in-case
```

You can delete these bookmarks later with `git branch -D backup-just-in-case`
once you're calm. Deleting a bookmark never deletes the commits it pointed at.

[Back to the decision table](index.md)
