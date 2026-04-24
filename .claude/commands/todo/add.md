---
description: Add a new TODO item to ROADMAP.md
allowed-tools: Read, Edit, Bash
---

# Add a TODO item

Add a new TODO item to the `## TODO` section in `ROADMAP.md` at the repo root.

## Input

The user provides a description of the TODO item as `$ARGUMENTS`. If no arguments are provided, ask the user what to add.

## Steps

1. Read `ROADMAP.md`. If it doesn't exist, offer to create one with a template skeleton (H1 + `last updated:` + `## TODO` with `<!-- next_id: 1 -->`).
2. Find the `## TODO` section.
3. Read the `<!-- next_id: N -->` comment to get the next available ID. If no such comment exists, use `1` and add the comment.
4. Add `- [ ] **N** $ARGUMENTS` as a new line at the end of the TODO checklist (before any blank line or next section).
5. Update the `<!-- next_id: N -->` comment to `<!-- next_id: N+1 -->`.
6. Update the `last updated:` timestamp at the top using `date '+%Y-%m-%d %H:%M'`.
7. Print confirmation: `Added TODO #N: $ARGUMENTS`.
