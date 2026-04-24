# Claude tooling

Repository-agnostic skills ported from a larger project, adapted so they work in any Claude-authored knowledge base.

## What's here

```
.claude/
├── standard/                 Conventions referenced from CLAUDE.md or on demand
│   ├── git-conventions.md    Conventional Commits format + rules
│   └── markdown-style.md     Wiki page structure, paper references, anchor slugs
└── commands/                 Slash-command definitions (invocable as /<name>)
    ├── callitaday.md         Summarize the current work streak from .claude/log.md
    ├── docs/
    │   └── full-read.md      Read every markdown file under docs/ in one pass
    └── todo/
        ├── fetch.md          List open TODOs from ROADMAP.md
        ├── add.md            Add a new TODO
        ├── complete.md       Mark a TODO done and move to the completed section
        └── delete.md         Remove a TODO that's no longer relevant
```

## Dependencies the ported skills assume

| Skill | Assumes on disk | What to do if absent |
|---|---|---|
| `/callitaday` | `.claude/log.md` (reverse-chronological session entries) | Create by convention; pair with a `/log` skill that writes to it. The skill will print "No log entries found" otherwise. |
| `/docs/full-read` | `docs/` directory populated with `.md` files | No-op if empty. |
| `/todo/*` | `ROADMAP.md` at repo root with a `## TODO` section | `/todo/add` offers to create the file on first use. |

None of these create runtime state beyond `.claude/cache/todo-list.txt` (regenerated on demand).

## How to wire them in

The slash-command files under `commands/` are auto-discoverable by Claude Code — invoking `/todo/fetch` loads `commands/todo/fetch.md` as context and follows its steps. Standards under `standard/` are not auto-loaded; reference them from your project's `CLAUDE.md` with something like:

```markdown
## Standardization

| Task | Standard | When to read |
|------|----------|-------------|
| Git commits | .claude/standard/git-conventions.md | Before committing |
| Writing doc pages | .claude/standard/markdown-style.md | Before creating or editing docs/ files |
```

## What was NOT ported

These skills exist in the source project but are too tied to that project's architecture to be generic:

- `/commit` — orchestrates `/log`, `/adr`, `/update-docs`, `/fetchtodo`, `/completetodo`. Port once you've decided which of those you want.
- `/docs/adr`, `/docs/update-docs`, `/docs/diataxis-split`, `/docs/repo-doc` — useful patterns but depend on specific folder layouts (e.g. `ds-concepts/`, `ds-tutorial/`, `ds-recipes/`, `ds-api-reference/`). Adapt by hand if you want them.
- `/overview:understand`, `/overview:update` — tied to a specific `.claude/PROJECT_OVERVIEW.md` pattern.
- Project-specific tutorials (`skill-canvas-node`, `skill-nodeset`, etc.) — domain-bound.

Port the ones you need when you need them. Most sessions only touch 1–2 skills at a time, and ad-hoc invocation beats pre-porting everything.
