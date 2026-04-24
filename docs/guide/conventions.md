# Conventions

The operating rules for this template. Read once, apply mechanically thereafter.

## 1. Filesystem IS the nav

Every folder under `docs/` that contains at least one `.md` file becomes a tab (top level) or a sidebar section (nested). Every `.md` file becomes a page. **Never edit `mkdocs.yml` to add pages.**

Consequence:

- Drop a new folder `docs/<x>/` with any `.md` inside → new tab appears.
- Drop a new `.md` into an existing folder → new sidebar entry.
- Rename a folder → nav label updates (with title-casing, see §3).

## 2. `.pages` files are for ordering and grouping *only*

Never use `.pages` to *add* pages. Files that exist on disk should be listed; files not on disk should not be listed. Use `.pages` for four things:

| Purpose | Syntax |
|---|---|
| **Order children** | `nav:` list with file/folder names in desired order |
| **Rename the tab / section** | `title: My Label` at top |
| **Group flat files into virtual sub-sections** | Nested `nav:` with labelled lists |
| **Include non-`.md` files** (e.g. `.html` decks) | Explicit entry in `nav:` |

If alphabetical order is fine and the folder name title-cases well, skip the `.pages` file entirely.

## 3. Two-to-five tabs is the sweet spot

One tab feels undercooked; six or more crowds the tab bar. Pick 2–5 top-level folders and stick to the plan.

Tab order is alphabetical by default. To force a custom order, create a root `docs/.pages`:

```yaml
arrange:
  - guide
  - recipes
  - reference
  - ...
```

Prefer not to — alphabetical is one less thing to maintain.

## 4. Root `/` redirects, not a root `index.md`

This template does **not** ship a `docs/index.md`. Instead `mkdocs-redirects` sends `/` → `guide/index.md` (configured in `mkdocs.yml`).

**Why**: a root `index.md` typically duplicates the nav (N links to N tabs) without adding value. Redirecting sends visitors straight into the content.

Alternatives if you prefer a landing page:

- Add `docs/index.md` (becomes the first tab, labelled from `site_name`) and remove the `redirects` plugin entry.
- Change the `redirects` target in `mkdocs.yml` to your preferred canonical page.

## 5. HTML / PPTX decks

`awesome-pages` only auto-discovers `.md` files. To surface a folder of `.html` decks:

1. Add a sibling `index.md` so the folder is recognised (without at least one `.md`, `awesome-pages` skips the folder).
2. List each `.html` explicitly in that folder's `.pages`:

```yaml
nav:
  - index.md
  - "Q1 Review": q1-review.html
  - "Supervisor Pitch": supervisor-pitch.html
```

## 6. Assets folders are invisible to the nav

Folders like `stylesheets/`, `images/`, `assets/` — anything without `.md` content — are skipped by `awesome-pages` and never become tabs. They still get copied to the built site by MkDocs; reference them via `extra_css`, `extra_javascript`, or regular Markdown image links.

## 7. `README.md` vs `index.md`

If your docs repo lives on GitHub, you may want a `README.md` at the docs root or inside a sub-folder. When both `README.md` and `index.md` exist at the same level, MkDocs emits a warning and **`index.md` wins** — `README.md` is excluded from the site.

This is the intended split:

- **`README.md`** — read on GitHub (scope, structure, how to contribute).
- **`index.md`** — read on the deployed site (landing / TOC for the tab).

Keep both.

## 8. Cross-folder links use relative paths

Internal links between pages use normal relative Markdown links:

```markdown
[Architecture](../guide/architecture.md)
```

When you restructure (move a folder), you **will** break cross-boundary links. Run `mkdocs build --strict` and the anchor checker in §9 to surface them.

## 9. Anchor links — beware slug drift

MkDocs slugifies headings like `## 1. Canvas & Editor` to `#1-canvas-editor` — ampersands and multiple spaces collapse to single dashes. Authors sometimes type `#1-canvas--editor` (double-dash) from memory, which breaks.

Fix: run

```bash
python scripts/check_anchors.py            # analyze
python scripts/check_anchors.py --apply    # rewrite source .md
```

It parses MkDocs' broken-anchor warnings, reads the built HTML for real anchor IDs, and proposes replacements via exact match → double-dash collapse → fuzzy similarity. Distinctive anchor strings (containing section numbers or tags) are safe to auto-apply; generic ones may want manual review first.

## 10. Strict build before committing

```bash
mkdocs build --strict
```

Upgrades broken-link warnings to errors. CI should run this too. Combine with `scripts/check_anchors.py` to auto-repair the most common drift class.
