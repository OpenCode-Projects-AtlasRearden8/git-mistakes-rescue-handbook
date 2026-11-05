# Chapter 5 — Detached HEAD Panic

*"I checked out an old commit to look at something, and now git keeps
saying `HEAD detached at 3f2a9c1` and I'm afraid to move."*

Deep breath. **Nothing is broken.** Git is telling you a simple fact:
you're standing on a commit like a platform, without a branch under your
feet. Picture tags on a wall of paintings: normally you stand on a
ladder with a name painted on it (a branch). Right now you're standing
directly on a painting (a commit id).

You are completely safe while *looking*. You are also safe while
*leaving*. The only danger zone is making commits here and then wandering
off and forgetting them — and even that is recoverable (Chapter 7).

## Do this first

Ask yourself one question: **did I make any commits while detached?**

### "No — I just looked around"

Just walk back:

```bash
git switch -
```

That means "take me to whatever branch I was on before" — git's version
of "undo my last teleport." (`git switch main` works too if you know the
branch you want.)

### "Yes — I want the commits"

Two moves, both safe. If the work is worth keeping, get it a branch name
*right now*, before anything else:

```bash
git switch -c rescued-commits
```

That creates a branch, right here, catching your new commits. Nothing is
lost; the commits now have a named ladder. You can rename the branch
later: `git branch -m rescued-commits a-better-name`.

### "Yes — but I want to throw them away"

Still make the safety bookmark first. Cheap, fast, invisible forever:

```bash
git branch just-in-case-detached
git switch -
```

## How does this even happen?

Totally ordinary ways:

- `git checkout 3f2a9c1` or `git checkout v2.3` to peek at an old state
  (looking at "what did it look like last week?" — a great use, not a
  crime).
- Clicking an old commit in a GUI tool.
- Checking out a tag.

None of these damage anything. Git's only warning label is "by the way,
any commits you make here won't belong to a branch."

## The one rule to tattoo somewhere

**Before leaving a detached HEAD you made commits on, run
`git branch save-name`.** A commit that no branch or tag points to is
still in the reflog for weeks, but why rely on memory — bookmark first.

## Common cross-panic

Sometimes people see "detached HEAD" right after a failed operation
(a bad rebase, a submodule oddity) and cannot tell *which* commit they're
sitting on. Answers:

```bash
git log --oneline -5      # what am I standing on?
git status                # is anything half-done?
```

Then choose "No — walk back" or "Yes — rescue" above. If `git status`
shows a rebase in progress, add the grace note from Chapter 8:
`git rebase --abort` puts everything back.

There's no such thing as being *stuck* in detached HEAD. It's a hallway,
not a trap. Every door you try leads somewhere recoverable.

[Back to the decision table](index.md)
