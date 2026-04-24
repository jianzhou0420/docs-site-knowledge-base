---
description: Read every markdown file under docs/ — full knowledge base ingest
allowed-tools: Read, Glob, Grep
---

# Full Read — the whole docs/ tree

Read all documentation under `docs/` in one pass. Glob-driven, so it survives restructures.

Use when you need the complete current state of the knowledge base — for Q&A, consistency checking, synthesizing a new cross-topic article, or grounding a big edit.

## Steps

### Step 1 — Index by top-level tab

Glob `docs/*` (directories only) to enumerate the top-level tabs. Skip:

- `docs/stylesheets/` (CSS, not content)
- Anything starting with `.` (`.pages`, `.obsidian`, etc. — config files)
- `docs/index.md` only if absent (this template redirects `/` via `mkdocs-redirects`)

For each tab folder, recursively glob `**/*.md` to get its file list. Print the count per tab before reading.

### Step 2 — Read per tab in parallel

For each tab folder, issue one parallel-batch Read for the files it contains. Prefer reading whole files when they're under 500 lines; for larger files, read the first 200 lines to get the intro + TOC, then chunk the body only if needed.

Read priority within each tab:
1. `index.md` first (gives you the tab's conceptual map).
2. Files whose names match a currently-relevant topic — use the user's prompt as a hint.
3. Remaining files, largest-first (big files usually carry the most load-bearing content).

### Step 3 — Present a summary

Structure the output:

- **Per-tab overview**: one sentence per tab naming what's in it and the file count.
- **Key terms / load-bearing concepts** encountered: a short glossary of terms the KB uses consistently.
- **Cross-tab references**: note where files in one tab link into another (strong coupling signals).
- **Thin / stub pages**: list files under 20 lines or containing `<!-- TODO` / `TBD` markers — these are authorial debt.
- **Inconsistencies**: flag contradictions, stale dates (`last updated:` lines > 60 days old), or terminology drift (same concept named differently across files).

### Step 4 — Suggest next actions

Based on what you read:

- **For authorial debt**: propose which stubs to fill next and why (frequency of incoming links is a good signal).
- **For inconsistencies**: propose which to reconcile first.
- **For missing connections**: suggest new pages or backlinks to add, with 1-sentence rationale each.

Do not take any of these actions without user confirmation — this command is read-only by design.

### Step 5 — Remind the user of related commands

- `/docs/full-read` — this command.
- `/todo/fetch` — open TODO items (if a `ROADMAP.md` exists).
- `/callitaday` — session summary (if `.claude/log.md` exists).
- To serve the site locally: `./run_dev.sh`.
