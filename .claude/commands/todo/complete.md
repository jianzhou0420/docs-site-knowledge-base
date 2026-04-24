---
description: Mark a TODO item as done in ROADMAP.md
allowed-tools: Read, Edit, Bash
---

# Complete a TODO item

Mark a TODO item as done in `ROADMAP.md`.

## Input

The user provides the TODO ID as `$ARGUMENTS` (e.g. `12`, `F3`). If no arguments are provided, ask the user which ID to complete.

## Steps

1. Read `ROADMAP.md`.
2. Find the line `- [ ] **<ID>** <description>` matching the given ID.
3. If not found, print `TODO #<ID> not found` and stop.
4. Change `[ ]` to `[x]` on that line.
5. Move the line to the end of a `## Completed TODO` section (create the section if it doesn't exist). Prefix with the completion date: `- [x] **<ID>** (completed YYYY-MM-DD) <description>`.
6. Update the `last updated:` timestamp at the top using `date '+%Y-%m-%d %H:%M'`.
7. Print confirmation: `Completed TODO #<ID>: <description>`.
