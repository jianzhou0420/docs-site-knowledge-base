# Add a tab to the doc-site

Create a new top-level tab under `docs/pages/<slug>/` — its `_tab.json`, a real landing
`index.html`, and (optionally) initial pages authored from the user's material — then bake
the chrome.

This skill is **self-contained**: the formats below are everything you need. Do not depend
on the shipped sample tabs (Guide/Recipes) — users delete those. The durable references are
the engine in `docs/_lib/` and any other tab's own `_tab.json`.

## Input

Arguments: `$ARGUMENTS` — free-form. May give a directory slug, a display label, an accent
key, and/or initial content. Examples:

- `reference "API Reference"`
- `add a Research tab, accent research, with a landing page about my reading list`

If the slug or label is unclear, ask **one** line. The slug is the URL segment
(`/pages/<slug>/…`); the label is the header text — they can differ.

## How a tab is defined

A tab is just a directory under `docs/pages/`. It needs at least an `index.html` (the
landing) so it isn't skipped, plus an optional `_tab.json` that controls presentation:

```json
{
  "label": "API Reference",
  "key": "architecture",
  "landing": "index.html",
  "order_priority": 30,
  "sections": [
    {"label": "API Reference", "dir": "", "key": "architecture", "order": ["index"]}
  ]
}
```

Field notes:

- **`label`** — header text (default: title-cased directory name).
- **`key`** — CSS accent class. Built-in ones in `docs/assets/style.css` include
  `guide`, `designdoc`, `capability`, `architecture`, `research`, `blueprint`, `glossary`,
  `roadmap`, `decisions`. Pick a fitting one (cosmetic only); or add your own accent vars.
- **`landing`** — page the tab opens to, relative to the tab dir (default `index.html`).
- **`order_priority`** — smaller = further left in the tab strip (default 100). Read the
  other tabs' `_tab.json` and choose a value that places this where the user wants; leave
  gaps (10, 20, 30 …).
- **`sections`** — sidebar groups. A section with `"dir": ""` points at the tab root, so a
  flat tab (pages directly in the dir) gets a sidebar; `order` pins the file-stem sequence.
  For a grouped tab, make subfolders and give each its own section (`"dir": "subfolder"`).
  Omit `sections` to auto-discover one section per subdirectory.

The landing `index.html` (and any page) follows the same document format as `/add-page`:
content only inside `<main class="doc-body">`, one `<h1>`, every `<h2>`/`<h3>` with a unique
`id`, no hand-written chrome, no site-name suffix in `<title>`.

## Steps

1. **Check** `docs/pages/<slug>/` does not already exist. If it does, stop and say so.
2. **Pick `order_priority`** by reading existing tabs' `_tab.json` (`ls docs/pages/*/_tab.json`),
   and choose an accent `key` (from the list above or one the user asked for).
3. **Write** `docs/pages/<slug>/_tab.json` using the schema above.
4. **Author** `docs/pages/<slug>/index.html` as a real landing page (the `/add-page` format):
   a genuine intro/hub for the tab — what it holds, links to its pages — not a stub.
5. **Optional initial pages** — if the user supplied material, author those pages too (same
   format) and add their slugs to the section's `order`.
6. **Bake the chrome**: `python3 docs/_lib/_wrap_handwritten.py`. (A tab with no serveable
   page is silently skipped, so `index.html` must exist before wrapping.)
7. **Report**: the tab now shows in the header; landing URL
   `http://0.0.0.0:8002/pages/<slug>/index.html`.

## Rules

- Author a real landing page; never ship an empty tab.
- Follow the page format exactly (one `<h1>`, `id` on every `<h2>`/`<h3>`, content only
  inside `<main class="doc-body">`, no chrome, no site-name suffix in `<title>`).
- Set `order_priority` deliberately so the tab lands where intended.
- Always run the wrap script last.
- If you need to confirm engine behavior, the authority is `docs/_lib/` — it always ships.
