# Doc-Site Conventions

The operating rules for this template. Read once, apply mechanically thereafter.

## 1. Filesystem IS the nav

Every folder under `docs/` that contains at least one `.md` file becomes a tab (top level) or a sidebar section (nested level). Every `.md` file becomes a page. **No editing `mkdocs.yml` to add pages.**

Consequence:

- Drop a new folder `docs/<x>/` with any `.md` inside → new tab appears.
- Drop a new `.md` into an existing folder → new sidebar entry.
- Rename a folder → nav label updates (with title-case, see §3).

## 2. `.pages` files are for ordering and grouping *only*

Never use `.pages` to *add* pages. Files that exist on disk should be listed; files not on disk should not be listed. Use `.pages` for four things:

| Purpose | Syntax |
|---|---|
| **Order children** | `nav:` list with file/folder names in desired order |
| **Rename the tab / section** | `title: My Label` at top |
| **Group flat files into virtual sub-sections** | Nested `nav:` with labelled lists |
| **Include non-`.md` files** (e.g. `.html` decks) | Explicit entry in `nav:` |

If alphabetical order is fine and the folder name title-cases well, skip the `.pages` file entirely.

## 3. Three top-level tabs is a convention, not a requirement

The template ships with **Developer Guide**, **Research**, **Knowledge Base** as top-level folders. Rename, add, or remove to match your project. Remember: each top-level folder is a tab, so don't proliferate — 3–5 tabs is the sweet spot.

Tab order is alphabetical by default. To force a custom order, create a root `docs/.pages`:

```yaml
arrange:
  - developer-guide
  - research
  - knowledge-base
  - ...
```

Prefer not to — alphabetical is one less thing to maintain.

## 4. Root / redirects, not a root index.md

`docs/index.md` is **not shipped** in this template. Instead `mkdocs-redirects` sends `/` → `developer-guide/core/blueprint.md` (configured in `mkdocs.yml`).

**Why**: a root index.md typically duplicates the nav (4 links to 4 tabs) without adding value. Redirecting sends visitors straight into the content.

If you want a welcome landing page, either:

- Add `docs/index.md` (becomes the first tab, labelled from `site_name`) and remove the `redirects` plugin entry, OR
- Change the `redirects` target in `mkdocs.yml` to your preferred canonical page.

## 5. HTML / PPTX decks

awesome-pages only auto-discovers `.md` files. To surface a folder of `.html` decks:

1. Add a sibling `index.md` so the folder is recognised.
2. List each `.html` explicitly in that folder's `.pages`.

See `docs/research/presentations/` for the pattern.

## 6. Assets folders (CSS, images) are invisible to nav

Folders like `stylesheets/`, `images/`, `assets/` — anything without `.md` content — are skipped by awesome-pages and never become tabs. They still get copied to the built site by MkDocs; reference them via `extra_css`, `extra_javascript`, or regular Markdown image links.

## 7. README.md vs index.md

If this doc-site repo lives on GitHub (or similar), you may want a `README.md` at the docs root. MkDocs + MkDocs Material handles the conflict: `README.md` and `index.md` at the same level produce a build-time warning, and `index.md` wins. **Keep both**: `README.md` for the GitHub view, `index.md` for the doc-site view.

## 8. Cross-folder links use relative paths

Internal links between pages use normal relative Markdown links:

```markdown
[Architecture](../core/architecture.md)
```

When you restructure (move a folder), you **will** break cross-boundary links. Run `scripts/check_anchors.py` and a strict build (`mkdocs build --strict`) to surface them.

## 9. Anchor links — beware slug drift

MkDocs slugifies headings like `## 1. Canvas & Editor` to `#1-canvas-editor` (ampersand and multiple spaces collapse to single dash). Authors sometimes type `#1-canvas--editor` (double dash) from memory — that breaks.

Fix: run `scripts/check_anchors.py` after renumbering sections. It parses MkDocs' broken-anchor warnings, reads the built HTML for real anchor IDs, and proposes replacements.

## 10. Strict build before committing

```bash
mkdocs build --strict
```

This upgrades broken-link warnings to errors. CI should run this too. The script at `scripts/check_anchors.py` covers the most common drift class automatically.
