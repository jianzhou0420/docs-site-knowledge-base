# Include an HTML deck

Rendered slide decks (Reveal.js, marp, PowerPoint → HTML export) are static `.html` files. `awesome-pages` only auto-discovers `.md`, so you have to list HTML explicitly.

## Steps

1. **Create a folder** to hold the decks. Place it wherever fits your nav — under a tab, or as its own tab.

   ```bash
   mkdir docs/recipes/decks
   ```

2. **Anchor it with an `index.md`.** Without at least one Markdown file, `awesome-pages` treats the folder as "no content" and skips it.

   ```bash
   cat > docs/recipes/decks/index.md <<EOF
   # Decks

   Rendered slide decks. Click to open.
   EOF
   ```

3. **Drop the HTML files in** and list them in `.pages`:

   ```
   docs/recipes/decks/
   ├── index.md
   ├── .pages
   ├── q1-review.html
   └── pitch.html
   ```

   ```yaml
   # docs/recipes/decks/.pages
   nav:
     - index.md
     - "Q1 Review": q1-review.html
     - "Supervisor Pitch": pitch.html
   ```

4. **Refresh.** The deck entries appear as sidebar links. Clicking opens the HTML file directly.

## Notes

- **PPTX source files** don't belong in `docs/` — they won't render and they inflate the build. Commit them in a separate `assets/` or `slides-src/` folder at the repo root, or store them elsewhere.
- **Large HTML decks** (multi-MB with embedded media) slow down `mkdocs build`; keep them under a few MB if you can.
- **Linking to a deck from Markdown**:
  ```markdown
  Watch the [Q1 review deck](decks/q1-review.html).
  ```
