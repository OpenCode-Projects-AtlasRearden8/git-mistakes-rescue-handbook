# Chapter 7 — "My Commit Vanished!"

*You ran a reset / rebase / amend / filter, and now `git log` just...
doesn't show your commit. Your stomach does a slow cold roll and you
wonder how long the last four hours takes to retype.*

This is the chapter that pays for the whole book, and it's short: **your
commit is almost certainly still on your disk, right now.** `git log`
isn't a census of every commit that exists — it only lists commits
reachable from your *current branch*. A commit your branch stopped
pointing at isn't destroyed; it's simply not being displayed. It's a
taped-over episode, not a burned film reel.

## Do this first (the real first move for nearly every panic)

```bash
git reflog
```

The reflog is git's private diary of everywhere your HEAD has ever been —
every commit, checkout, reset, merge, rebase landing spot — kept locally
on your machine (for months by default). It is the closest thing git has
to an undo button.

You'll see lines like:

```
3f2a9c1 HEAD@{0}: reset: moving to origin/main
a8b1e77 HEAD@{1}: commit: add the tricky parser fix
9c4d552 HEAD@{2}: commit (amend): tidy up docs
```

Read down the list and find the line *before* the disaster — here, the
fix commit `a8b1e77` sitting at `HEAD@{1}`. Then:

```bash
git branch rescue a8b1e77      # bookmark it (recommended first move)
git reset --hard a8b1e77      # or: move your branch back to it
```

Congratulations: the "vanished" commit is back and your log is now
*showing* it. You didn't resurrect anything. You just pointed your branch
at where it had been all along.

The same trick works no matter what the words after `HEAD@{n}:` say —
`reset`, `checkout`, `rebase`, `pull`, `amend`. If the position is in the
reflog, your branch can point there again. For rebases gone sideways,
`HEAD@{1}` is usually the pre-rebase you; for a bad pull, likewise. All
roads lead to reflog.

## "I ran `git rebase` (or `pull --rebase`) and my commits disappeared"

```bash
git reflog
git reset --hard HEAD@{1}
```

Two lines. Read the reflog, confirm `HEAD@{1}` says something like
`rebase (start): ...` followed by your work before it — actually, read
for the *commit line* below the rebase entries, which lists where your
commits were living. When in doubt, bookmark several nearby entries as
separate branches and eyeball `git log --oneline` on each. Brute force,
zero risk.

## "I made a typo in a commit message and panicked"

```bash
git commit --amend -m "correct message"
```

That rewrites only the *latest* commit, which is safe before you push. If
you've already pushed and nobody's reviewed it yet, amend + push again is
acceptable. If it's buried under other commits or already shared:
`git rebase -i` can reword it, but that's history rewriting — on shared
branches, let the typo live and read Chapter 6's Rule 1.

## "I amended over my own good commit / reset away the good one"

Same door as always: `git reflog`, find the pre-disaster entry, bookmark,
reset. Amend keeps the *old* commit alive in the reflog; it never
vanishes either.

## "My stash popped and blew away other work"

```bash
git stash apply --index stash@{1}
```

or, cleaner, going forward in time: the popped stash is still a commit
in the reflog — search for `git stash: WIP on` and apply it anew. If
git complained "Your local changes would be overwritten," your work
wasn't even touched; git refused first.

## Why this works (the 90-second theory)

Git keeps every commit as an object with a permanent id, written into
your repository's object store, until either (a) garbage collection
prunes unreachable ones after their default grace period (typically
weeks), or (b) someone deliberately and aggressively wipes the repo.
Between "the branch stopped pointing at it" and "pruned-ish eventually,"
there's a months-long runway. Reflog is your map of that runway. Rescue
is: find id → point a branch at it → done.

The single habit that makes all of this automatic: **run `git reflog`
before you believe anything is gone.** It's the difference between
"retype four hours" and "bookmark two ids."

[Back to the decision table](index.md)
