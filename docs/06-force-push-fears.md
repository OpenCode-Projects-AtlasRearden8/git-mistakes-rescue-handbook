# Chapter 6 — Force-Push Fears

*"I've heard force-pushing can destroy your teammates' work, and I have...
feelings about running it."*

Good instincts! Out of everything in this book, this is the one command
that can genuinely damage other people's work. So let's be honest and
precise, and then give you rules you can hold onto.

## What a force-push actually does

Normally, `git push` refuses if the remote branch has commits you don't
have — git says "you should pull first" and that refusal *protects*
people. `git push --force` means "my local version wins; delete whatever
is on the remote that I don't have." Whatever the remote had that you
didn't is no longer pointed at by the branch. (Not instantly destroyed —
Chapter 7 explains why — but invisible to your team members.)

## The rules, in order of importance

### Rule 1: Never force-push a branch other people use

Main branches, shared feature branches, anything with teammates: don't
force-push there. Plain never. If history on a shared branch needs fixing
(mistaken secret committed, wrong merge), the polite tool is `git revert`
— it *adds* an undoing commit and rewrites nothing. Everyone's clones
keep working. That's it. That's the whole safe answer for shared history.

### Rule 2: Force-pushing *your own* branch is normal and fine

If you squashed/rebased your own feature branch before opening a pull
request, a force-push to *that* branch is routine. It's your branch.
Nobody else is standing on it. It doesn't touch main, history, or anyone
else's work.

### Rule 3: If you must force-push, use `--force-with-lease`

```bash
git push --force-with-lease
```

This is the seatbelt version. Plain `--force` is "override, no
questions." `--force-with-lease` says: "override, **but only if the
remote still looks like what I last saw**." If a teammate pushed
something you haven't seen, the push *refuses* instead of vaporizing
their new commits. Make it your habit word. There is no downside.

### Rule 4: Write hooks can differ; the branch guard exists

On hosting sites (GitHub, GitLab, etc.) you'll sometimes hit "protected
branch" — the server itself *forbids* force-pushes to main even if you
type the wrong flag. That protection is your friend; leave it on.

## "Oh no, I already force-pushed and lost someone's commits"

Immediate triage, no blame, recover the commits:

1. **Ask the person, kindly.** Their machine still has the original
   commits in their local repo. `git push` from there (or open a branch)
   restores everything. This is the usual happy ending.
2. **Check the host.** Most forges keep a reflog/activity log and may
   allow restoring the branch from the web UI or show dangling commits.
3. **You still have the old id.** If anyone saved the commit id (from a
   terminal scrollback, a code-review email, CI logs), then on the remote
   clone: `git branch restore-branch the-old-id && git push -u origin
   restore-branch`. Chapter 7 explains why this works: commits aren't
   destroyed by losing a branch name; they're orphaned, and you can
   re-adopt them by id.

## Your force-push preflight checklist

Before typing any push with force in it, ask:

- [ ] Does anyone else use this branch? (If yes → revert instead.)
- [ ] Did I make a bookmark first? (`git branch backup-before-force`)
- [ ] Am I using `--force-with-lease`, not bare `--force`?
- [ ] Do I have the old commit id written down somewhere? (Copy the
      output of `git rev-parse HEAD` into a notes file. Thirty seconds of
      paranoia insurance.)

Four ticks and a click. And most days, thanks to Rule 1 and Rule 3, the
"force-push fears" chapter of your life will just be... one flag you
always type out of habit, and a revert when team history needs adjusting.

*(This handbook is a friendly explainer, not official documentation of
any hosting service's exact behavior — server protections vary. When in
doubt on a shared repo: ask your team before rewriting anything.)*

[Back to the decision table](index.md)
