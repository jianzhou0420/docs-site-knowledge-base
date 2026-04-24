---
description: Remove a TODO item from ROADMAP.md (use when the item is no longer relevant)
allowed-tools: Read, Edit, Bash
---

# Delete a TODO item

Remove a TODO item from `ROADMAP.md`. Use this only when the item is **no longer relevant** (not when it's completed — use `/todo/complete` for that).

## Input

The user provides the TODO ID as `$ARGUMENTS` (e.g. `12`, `F3`). If no arguments are provided, ask the user which ID to delete and why.

## Steps

1. Read `ROADMAP.md`.
2. Find the line `- [ ] **<ID>** <description>` matching the given ID.
3. If not found, print `TODO #<ID> not found` and stop.
4. **Confirm with the user** before deleting — a one-line prompt showing the item's description is enough. Deletion is irreversible (git history aside).
5. On confirmation, remove the line entirely.
6. Update the `last updated:` timestamp at the top using `date '+%Y-%m-%d %H:%M'`.
7. Print confirmation: `Deleted TODO #<ID>: <description>`.
