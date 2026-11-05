# Pocket Card — Panic Commands at a Glance

Print this, screenshot it, glue it to your monitor. Each line is the
shortest safe version of its rescue; each chapter explains it fully.

| Panic | Calm move | Chapter |
| --- | --- | --- |
| Fear committing messy work | `git add -A && git commit -m "wip"` | [Ch 1](01-uncommitted-work.md) |
| Keep work, tidy directory | `git stash` (then `git stash pop`) | [Ch 1](01-uncommitted-work.md) |
| Started editing on wrong branch | `git switch -c right-branch` | [Ch 2](02-wrong-branch.md) |
| Committed to wrong branch | bookmark, then `git reset --hard <old-main>` | [Ch 2](02-wrong-branch.md) |
| Open merge conflicts, regretting | `git merge --abort` | [Ch 3](03-bad-merge.md) |
| Merge already completed | `git reset --hard ORIG_HEAD` | [Ch 3](03-bad-merge.md) |
| Bad merge already pushed | `git revert -m 1 <merge-id>` | [Ch 3](03-bad-merge.md) |
| Staged everything by accident | `git restore --staged .` | [Ch 4](04-staged-changes.md) |
| "HEAD detached" message | `git switch -` (or `git switch -c keep-it`) | [Ch 5](05-detached-head.md) |
| Must touch shared history | `git revert`, never force-push | [Ch 6](06-force-push-fears.md) |
| Force-push your own branch only | `git push --force-with-lease` | [Ch 6](06-force-push-fears.md) |
| "My commit vanished" | `git reflog`, then bookmark + reset | [Ch 7](07-vanished-commit.md) |
| Total confusion | `git status` + `git branch backup-*` + `git reflog` | [Ch 8](08-safety-net.md) |
| Mid rebase/merge chaos | `git rebase --abort` / `git merge --abort` | [Ch 8](08-safety-net.md) |
| Ultimate fallback | `cp -r myproject ../myproject-snapshot` | [Ch 8](08-safety-net.md) |

**Before anything scary:** `git branch backup-just-in-case`
**Before believing anything is gone:** `git reflog`
[Back to the decision table](index.md)
