# Quick Start

Assumes you have [installed](installation.md) the template and are running `./run_dev.sh`.

## 1. Rename the site

Open `mkdocs.yml` and replace `site_name` and `site_description`:

```yaml
site_name: My Project Docs
site_description: "Short tagline"
```

Save — the dev server reloads automatically.

## 2. Replace the landing page

The root URL `/` redirects to `guide/index.md` by default. You have two choices:

- **Edit this page** (`docs/guide/index.md`) to be your project's welcome page.
- **Change the redirect target** in `mkdocs.yml`:

  ```yaml
  plugins:
    - redirects:
        redirect_maps:
          'index.md': 'your/landing/page.md'
  ```

## 3. Add content

### Add a page

Drop a Markdown file anywhere inside `docs/`:

```bash
touch docs/guide/architecture.md
```

Refresh the browser — the page appears in the **Guide** sidebar at the bottom, alphabetically.

To control where it sits, edit `docs/guide/.pages`:

```yaml
nav:
  - index.md
  - Installation: installation.md
  - Architecture: architecture.md    # ← new entry
  - Quick Start: quick-start.md
  ...
```

### Add a tab

Drop a new top-level folder under `docs/` with at least one `.md` inside:

```bash
mkdir docs/reference
echo "# Reference" > docs/reference/index.md
```

Refresh — a **Reference** tab appears (alphabetical ordering by default).

### Rename a tab

Create or edit `docs/<folder>/.pages`:

```yaml
title: My Preferred Label
```

Folder name → tab slug (used in URLs). `title:` → tab label (shown in the nav bar). They can differ.

## 4. Ship

```bash
mkdocs build --strict
```

Copy `site/` to any static host (GitHub Pages, Netlify, S3, nginx). See [Installation — Build](installation.md#build-a-static-site) for options.

## Next

- [Why this pattern](why.md) — understand the tradeoffs before deviating.
- [Conventions](conventions.md) — the full ruleset.
- [Recipes](../recipes/index.md) — common tasks with worked examples.
