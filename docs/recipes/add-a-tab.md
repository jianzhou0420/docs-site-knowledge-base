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

## Importing an external KB as a tab (git submodule)

If a knowledge base lives in its own repo — maybe you split a topic out for independent history, or you want to share it between sites — pull it in as a submodule under `docs/`.

```bash
git submodule add https://github.com/<owner>/<kb-repo>.git docs/<folder>
```

Awesome-pages picks it up as a tab automatically. If the external repo carries its own `.pages` with a `title:`, that becomes the tab label; otherwise it's the folder name.

**Worked example — shipped with this template.** The `kb-vln` tab you see in the dev server is exactly this pattern:

```bash
git submodule add https://github.com/jianzhou0420/kb-vln.git docs/kb-vln
```

`kb-vln` ships its own `.pages` with `title: Knowledge Base`, so the tab reads "Knowledge Base" rather than "Kb Vln". Cloning this template with `--recurse-submodules` brings it along for free — giving you a working, content-rich tab to poke at before you write your own.

To update the imported content later:

```bash
cd docs/<folder> && git pull origin main && cd - && git add docs/<folder> && git commit -m "chore: bump <folder> submodule"
```

## Removing a tab

Delete the folder. If anything else linked to it, those links will now 404 — run `mkdocs build --strict` to find them.

If you want to preserve old URLs (for incoming bookmarks), add a redirect in `mkdocs.yml`:

```yaml
plugins:
  - redirects:
      redirect_maps:
        'reference/index.md': 'guide/index.md'
```
