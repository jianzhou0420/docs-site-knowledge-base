# Why this pattern

## The problem it solves

A traditional MkDocs site keeps its nav tree inside `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Guide:
    - Installation: guide/installation.md
    - Architecture: guide/architecture.md
    ...
```

Every new page means two edits: create the Markdown file, and wire it into the nav. For small sites this is fine. Once the nav crosses ~40 entries and multiple contributors touch it, several frictions compound:

- **Merge conflicts on `mkdocs.yml`** every time two people add pages in parallel.
- **Drift between filesystem and nav** — files exist but are never added; nav entries point at missing files.
- **Renames and moves require three edits** (file, nav path, any cross-link) and people forget the nav one.
- **Reviewing the nav as a single YAML block** becomes unwieldy; you can't see which tab owns what.

## What this template does instead

Three plugins swap the source of truth:

| Plugin | Effect |
|---|---|
| `awesome-pages` | Nav comes from the filesystem. Every folder under `docs/` that contains Markdown becomes a tab or section. Every `.md` becomes a page. |
| `mkdocs-redirects` | The bare URL `/` redirects to a canonical landing page. No root `index.md` to maintain. |
| Per-folder `.pages` YAML | Opt-in overrides when alphabetical/title-cased defaults are wrong. Local to the folder — no global config. |

Result: **adding content becomes a one-step action**. Create the file or folder, commit. No nav edit.

## The tradeoffs — honest version

This is not free. You accept:

- **Less central control.** The nav isn't a single file you can audit in one glance. If that's important for your workflow (compliance, review process), keep explicit `nav:` instead.
- **Slug = filename.** Page URLs derive from filenames. Rename a file = break its URL. Use [`mkdocs-redirects`](https://github.com/mkdocs/mkdocs-redirects) for renames you need to honor.
- **`.pages` is a second config surface.** You go from *one* centralized nav file to *N* per-folder overrides. In aggregate it's less code, but the code is more scattered.
- **Plugin risk.** `awesome-pages` is actively maintained but is a third-party plugin. If it were abandoned, you'd either maintain a fork or migrate back to an explicit nav (straightforward but annoying).

## When this pattern shines

- **Docs tree with 50+ pages** edited by multiple people.
- **Frequent reorganization** — you move folders around as your project evolves.
- **Research / knowledge-base style content** where the "right" structure isn't known in advance.

## When it doesn't

- **< 10 pages** — explicit `nav:` is simpler and more transparent for readers of your config.
- **Strict review requirements** where every nav change must be a single diffable commit.
- **i18n** — `awesome-pages` doesn't model translations; pair with `mkdocs-static-i18n` carefully, or keep explicit `nav:` for clarity.
