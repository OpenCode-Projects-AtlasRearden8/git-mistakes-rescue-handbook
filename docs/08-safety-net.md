# Chapter 8 — The Universal Safety Net

*"I don't even know what I did. Something feels wrong and I'm scared."*

This is the "I have no idea" chapter for total confusion. No diagnosis needed. Three
moves, in order. They are read-only or bookmark-only, which means they
cannot make anything worse.

## Do these first — always, every panic, in this order

```bash
git status
```
Read-only. Tells you what state git thinks you're in and names anything
in progress (merge, rebase, cherry-pick...).

```bash
git branch backup-right-now
```
Creates a bookmark pointing at your current position. Committing
nothing, changing nothing. Whatever commits you're standing on are now
immortal-by-name.

```bash
git reflog
```
The diary. Almost every "lost" moment ends with an entry in here. Find
where you were before things went sideways.

Then — and only then — decide something. When you're calm, that's when
the other chapters apply: uncommitted chaos (Chapter 1), branch surgery
(Chapter 2), merge undo (Chapter 3). All of them become easy once a
bookmark points at where you stand.

## If a rebase or merge is mid-flight and scaring you

The sky is still up there. Abort is allowed at any pause point:

```bash
git merge --abort
git rebase --abort
git cherry-pick --abort
```

Whichever operation `git status` names. Abort returns your branch to its
pre-operation position. You lose nothing but the half-done operation.

## If you touched `--force` and need to calm down

Read Chapter 6 immediately (mostly reassurance there), and know the two
facts that de-escalate everything: (1) force-pushing only detaches the
remote *label*; commits still exist locally on someone's machine until
garbage collection, and (2) `--force-with-lease` exists specifically to
stop tomorrow's version of this fear.

## If it says a file has secrets in it

Short version: staged-but-uncommitted → unstage and you're fully clean.
Already committed → treat the secret as exposed, replace/rotate it (the
value itself, not just the file), then clean history later when calm
(`git filter-repo` in a spare copy, never on your only clone, never
hungry). The rotation matters more than the deletion — that's the actual
security rule, and it applies to real credentials and fake examples
alike.

Note the spirit of this handbook: we avoid printing working credential
examples at all, so nothing here can ever leak. Model the habit in your
own docs: name files, never values.

## The nuclear-but-permanent fallback

There is one universally safe move that works even when git itself
confuses you: copy the folder.

```bash
cp -r myproject ../myproject-snapshot-$(date +%H%M)
```

Now there are two of your project. Git experiments can rage in one while
the other sits untouched. Nothing in this handbook requires it — but
knowing it exists means you're never cornered. (Yes, this works even
mid-rebase, mid-anything. Files are files.)

## The calm summary

- `git status`, `git branch backup-*`, `git reflog` — read-only, always
  safe, always first.
- `--abort` flags — official off-switches, allowed anytime operations
  pause.
- Chapter 7's reflog bookmark-and-reset — the universal "undo my last
  clever idea."
- Folder copy — the zero-trust safety net that never fails.

You now know more about git panic than most people who've used git for
years. The secret was never knowing all 150 subcommands. It was knowing
four safe moves and that almost nothing is actually destroyed.

[Back to the decision table](index.md)
