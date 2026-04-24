# Add a tab

## Minimum steps

```bash
mkdir docs/reference
echo "# Reference" > docs/reference/index.md
```

Refresh. A **Reference** tab appears in the top bar. Alphabetically ordered by default.

## Controlling tab order

Tabs sort alphabetically. To force a custom order, create `docs/.pages`:

```yaml
arrange:
  - guide
  - recipes
  - reference      # ← placed third instead of alphabetical
  - ...
```

The `...` catch-all (optional) lets any unlisted folders fall through. Useful during restructures.

## Giving the tab a non-slug title

Folder name determines the URL slug (`/reference/...`). Tab label defaults to title-cased folder name. Override the label via `docs/<folder>/.pages`:

```yaml
title: My Reference
```

Result: URL stays at `/reference/...`, tab reads "My Reference".

## Removing a tab

Delete the folder. If anything else linked to it, those links will now 404 — run `mkdocs build --strict` to find them.

If you want to preserve old URLs (for incoming bookmarks), add a redirect in `mkdocs.yml`:

```yaml
plugins:
  - redirects:
      redirect_maps:
        'reference/index.md': 'guide/index.md'
```
