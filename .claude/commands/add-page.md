# Add a page to the doc-site

Author a new content page under `docs/pages/<tab>/` as real HTML — derived from the user's
topic or source material, not an empty skeleton — then wire it into the tab and bake the
chrome. This is the Claude-as-author path: read the source, structure it, cross-link it.

This skill is **self-contained**: everything you need to produce a correct page is below.
Do not depend on the shipped sample pages (Guide/Recipes) — users delete those. The only
durable references are the engine in `docs/_lib/` and the target tab's own `_tab.json`.

## Input

Arguments: `$ARGUMENTS` — free-form. May name a tab, a page title/topic, and (optionally)
source material or a path to it. Examples:

- `guide Architecture`
- `add a page to the guide tab that summarizes notes/caching.md as "Caching model"`
- `research "Reading list: world models"`

If the target tab or the page title is unclear, ask **one** line. To list existing tabs:
`ls -d docs/pages/*/`.

## The page format (author exactly this shape)

A page is a complete, standalone HTML document. Your authored content goes **only** inside
the single `<main class="doc-body">` block; the wrap script (step 4) generates all the
chrome — header, sidebar, breadcrumbs, on-this-page TOC, footer — around it.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Caching model</title>
</head>
<body>
<main class="doc-body">
<h1>Caching model</h1>

<p>Lead paragraph …</p>

<h2 id="how-it-works">How it works</h2>
<p>…</p>

<h3 id="invalidation">Invalidation</h3>
<p>…</p>
</main>
</body>
</html>
```

Format rules:

- **Content only inside `<main class="doc-body">`.** Never write any header / sidebar /
  breadcrumb / footer markup — the wrap script owns the chrome and will inject it.
- **`<title>`** = the page title, with **no** site-name suffix. The wrapper appends
  " — &lt;site&gt;" itself, and derives the sidebar/breadcrumb label from the `<h1>`.
- **Exactly one `<h1>`** — it is the page title.
- **Every `<h2>` and `<h3>` gets a unique `id`** (kebab-case slug of its text), e.g.
  `<h2 id="how-it-works">`. The right-hand on-this-page TOC is built from these; headings
  without an `id` are skipped.
- Use ordinary HTML for body content: `<p>`, `<ul>`/`<ol>`, `<table>`, `<pre><code>…</code></pre>`,
  `<strong>`, `<code>`. Cross-link related pages with relative hrefs ending in `.html`
  (`<a href="other.html">`, `<a href="../tab/page.html">`).
- Page-specific `<style>` (in the head) and trailing `<script>` blocks are preserved across
  wraps if you need them.

## Steps

1. **Resolve the target tab** `docs/pages/<tab>/`. If it doesn't exist, suggest `/add-tab`
   and stop.
2. **Pick a slug** — a kebab-case filename stem from the title ("Caching model" →
   `caching-model`). Avoid colliding with existing files in the tab.
3. **Author** `docs/pages/<tab>/<slug>.html` using the format above, with **real content**
   derived from the user's topic/source: organize it well, write prose, optimize headings
   and flow, add cross-links. (Optional: if sibling pages exist, you may glance at one to
   match house style — but never rely on a specific page being present.)
4. **Wire into nav** — open `docs/pages/<tab>/_tab.json` and add `<slug>` to the relevant
   section's `order` array at a sensible position (or append). A section with `"dir": ""`
   covers the tab root. If the tab has no `order` (auto-discovery), nothing to edit.
5. **Bake the chrome**: `python3 docs/_lib/_wrap_handwritten.py` (if `run_dev.sh` is already running it auto-wraps, but running it explicitly is always safe and idempotent).
6. **Report**: the URL `http://0.0.0.0:8002/pages/<tab>/<slug>.html`, and confirm the page
   now appears in the sidebar in the intended position.

## Rules

- Produce real, useful content. If given source material, summarize / structure / cross-link
  it; never ship an empty stub when content was provided.
- Follow the format block exactly: one `<h1>`, every `<h2>`/`<h3>` has an `id`, content only
  inside `<main class="doc-body">`, no hand-written chrome, no site-name suffix in `<title>`.
- Always run the wrap script last.
- Don't modify other pages' authored content (editing `_tab.json` is fine).
- If you ever need to confirm exactly what the wrapper expects, the authority is the engine
  in `docs/_lib/` (`_wrap_handwritten.py`, `_layout.py`) — it always ships.
