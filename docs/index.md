# The Git Mistakes Rescue Handbook

*A beginner manual for recovering from git panic — by Asdale Dynamics, LLC*

Git has a reputation for being scary. It isn't, really. It's just a very
literal diary of your project, and almost every "I've ruined everything"
moment in git is reversible. Git is designed to **not lose your
work**. The hard part is knowing which few commands get you back to safety.

This handbook is written like a friend explaining it across the kitchen
table: plain English, step by step, never condescending. Every chapter
starts with "what you're feeling," tells you the **one thing to do first**,
and then walks through the fix calmly.

**The golden rule of git panic: don't delete anything, don't re-clone, and
don't run anything with `--force` until you've read one chapter of this
book. Your work is almost certainly still on your disk.**

## How to use this book

1. Find your situation in the decision table below.
2. Read the one-line "do this first" move.
3. Open the linked chapter, breathe, follow the steps.

You never need to memorize anything. Git experts don't memorize either —
they just know this table by heart.

---

## The decision table: "what did you just do?"

| What just happened (how it feels) | What's really going on | Do this first | Full walkthrough |
| --- | --- | --- | --- |
| "I have a half-finished mess and I'm scared to commit it" | Work-in-progress in your working directory | `git add -A` then `git stash` — or just commit it to a branch | [Chapter 1 — Uncommitted Work](01-uncommitted-work.md) |
| "I'm on the wrong branch and I already started editing" | Uncommitted work on the wrong branch | `git switch -c better-branch` (your edits come with you) | [Chapter 2 — Wrong Branch](02-wrong-branch.md) |
| "I committed to the wrong branch" | Commits sitting on the wrong branch tip | `git branch correct-branch && git reset --hard origin/wrong-branch-name` — read the chapter first | [Chapter 2 — Wrong Branch](02-wrong-branch.md) |
| "I merged and it went horribly wrong" | A merge commit (or conflict mess) you regret | `git merge --abort` if conflicts are open; otherwise `git reset --hard ORIG_HEAD` | [Chapter 3 — Bad Merge](03-bad-merge.md) |
| "I staged everything / staged the wrong things" | Things sitting in the staging area | `git restore --staged .` to unstage everything | [Chapter 4 — Staged Changes Panic](04-staged-changes.md) |
| "It says HEAD is detached and I panicked" | You're peeking at an old commit, not on a branch | `git switch -` (go back) or `git switch -c new-branch` (keep the work) | [Chapter 5 — Detached HEAD](05-detached-head.md) |
| "I'm scared of force-pushing and breaking the team's history" | Push rewriting a shared branch | Don't. Use `--force-with-lease` only if you must; read the chapter first | [Chapter 6 — Force-Push Fears](06-force-push-fears.md) |
| "My commit vanished! It's not in the log!" | Probably in the reflog, and it is *not* gone | `git reflog` — every rescue starts here | [Chapter 7 — My Commit Vanished](07-vanished-commit.md) |
| "Something else / total confusion" | Unknown; work is probably still safe | Run the three safety commands in Chapter 8 | [Chapter 8 — The Universal Safety Net](08-safety-net.md) |

---

## Three habits that end 90% of future panics

1. **Commit early, commit ugly.** A commit named "wip messy draft" on a
   throwaway branch costs you nothing and saves everything. Nobody grades
   your commits.
2. **Make a "backup branch" before anything scary.** `git branch backup-just-in-case`
   before you rebase, reset, or merge. It's a bookmark pointing at where you
   are *right now*, and you can never lose anything the bookmark points to.
3. **Learn `git reflog`, not `--force`.** The reflog (Chapter 7) is git's
   own undo button. Almost every "vanished" disaster is a two-command fix.

## What this book is not

- It is not exhaustive. It covers the panics, not all 150 subcommands.
- It is not medical, legal, or financial advice — and it's not even
  official git advice. It's experience, explained plainly. When in doubt,
  make a backup branch and copy your folder somewhere safe first.
- It never asks you to trust a command blindly. Every chapter explains
  what the command actually does before you run it.

Ready? Find your row in the table above. You've got this.
