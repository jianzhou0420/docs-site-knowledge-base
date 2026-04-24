---
description: Print the current open TODO list from ROADMAP.md, with caching
allowed-tools: Read, Write, Bash
---

# Fetch TODO list

Print the current open TODO list from `ROADMAP.md` at the repo root.

## Cache

- Cache file: `.claude/cache/todo-list.txt`
- First, run a **cache-check** via Bash (output only, no rendering):
  ```
  [ -f .claude/cache/todo-list.txt ] && [ .claude/cache/todo-list.txt -nt ROADMAP.md ] && echo HIT || echo MISS
  ```
- On **HIT**: use the `Read` tool on `.claude/cache/todo-list.txt`, then **reprint the full contents verbatim as assistant message text** (inside a fenced code block). Do **not** use `cat` — its output gets folded in the conversation UI. Skip the regenerate steps.
- On **MISS**: regenerate (steps below), write to the cache, then reprint the rendered block as assistant message text (same no-`cat` rule).

## Regenerate (cache miss)

1. Read `ROADMAP.md`.
2. Collect all `[ ]` (open) items from the `## TODO` section. Skip `## Completed TODO` (or `## Done`) and any `[x]` items entirely.
3. If `ROADMAP.md` groups TODOs by category (e.g. `## TODO`, `## Feature TODO`, `## Research TODO`), collect all open items across those sections.
4. Build each line showing **ID**, optional **scope tag**, and brief description:
   ```
   [ ]   1  docs         rewrite getting-started for conda
   [ ]   2  kb           add synthesis skill for cross-topic summaries
   [ ]   3  infra        wire up GitHub Pages deploy
   ```
   Scope tags are conventional and project-defined — keep them short.
5. If there are multiple sections, group by section with headers:
   ```
   --- TODO (N open) ---
   ...
   --- Feature TODO (N open) ---
   ...
   ```
6. Append a summary line: `N open total`
7. Write the full rendered block to `.claude/cache/todo-list.txt`, then print it.

## Invalidation

`/todo/add`, `/todo/complete`, `/todo/delete`, and any manual edit to `ROADMAP.md` update its mtime, which naturally invalidates the cache on the next fetch. No explicit invalidation needed.

## Edge case: no ROADMAP.md

If `ROADMAP.md` does not exist, print:
```
No ROADMAP.md found at repo root. Create one with a "## TODO" section to start tracking.
```
