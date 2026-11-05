# Chapter 1 — Uncommitted Work Panic

*You have a half-finished mess in your project and you're afraid to touch
anything: afraid to commit it, afraid to switch branches, afraid to close
your laptop.*

Good news first: **uncommitted work is the safest state to panic in.**
Nothing has been rewritten. Git hasn't done anything subtle. Your edits
are ordinary files sitting on your disk, right now, exactly where you left
them.

## Do this first

Just look. Type:

```bash
git status
```

Nothing there deletes or changes anything. `git status` is a camera, not
a tool. Read what it says — it literally names the sections you're worried
about: *Changes to be committed*, *Changes not staged for commit*,
*Untracked files*. Those are all your files, and they're all still yours.

## Your three options (all safe)

### Option A: Commit it, messy on purpose

A commit is a save point, not a publication. Nobody grades it.

```bash
git add -A
git commit -m "wip: messy draft before i figure this out"
```

You can clean it up later (squash it, reword it, or throw the whole thing
away). A messy commit you delete tomorrow is infinitely better than work
you lose today.

Tip: if your editor ghost-wrote a giant commit message you didn't want,
you can fix it immediately with `git commit --amend` — see Chapter 7's
"amend" note for when that's safe.

### Option B: Stash it (a couch cushion for your work)

`git stash` scoops up all uncommitted changes and puts them in a private
pile, then tidies your working directory back to the last commit.

```bash
git stash          # scoop it all up
git stash list     # see the pile
git stash pop      # put it back when you're ready
```

The stash is *not* garbage-collected for a long time, so even a stash you
forgot about for weeks can usually be recovered (see Chapter 7 if you
popped something over other changes by mistake).

One caution: `git stash` can feel like magic, and the pile is invisible.
If you're the kind of person who reads papers at the bottom of backpacks
three years later, Option A (commit) will suit you better.

### Option C: Do nothing, but nothing dumb

Uncommitted work survives: closing your editor, rebooting, even most
branch switching. It does **not** survive `git reset --hard` or
`git checkout -- .`. So while you're deciding:

- Don't run anything with `reset` in it.
- Don't run anything with `checkout --` or `restore` (file mode) in it.
- Make a folder copy if you want a purely non-git safety net:
  `cp -r myproject myproject-a-copy`. Crude, effective, yours.

## "But I deleted files and now `git status` shows deletions"

Deletions you haven't committed are also just... changes. Bring files back:

```bash
git restore path/to/deleted-file
```

`git restore` (asked politely) simply re-copies the file from the last
commit. It can't resurrect a file that was never committed, though — which
is the realest reason to commit early, commit ugly.

## The one-minute habit

Before every coffee break: `git add -A && git commit -m "wip"`.
Commits are free. Lost evenings are not.

[Back to the decision table](index.md)
