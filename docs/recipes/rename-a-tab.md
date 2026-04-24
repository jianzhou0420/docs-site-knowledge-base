# Rename a tab

Two different things people call "rename a tab":

## A. Change the label, keep the URL

The label shown in the nav bar is separate from the folder name (which drives the URL). To change only the label:

Edit `docs/<folder>/.pages`:

```yaml
title: Developer Handbook        # was "Guide"
```

No file moves. Existing links work. Done.

## B. Change the URL too

You want the URL to change from `/guide/...` to `/handbook/...`. Rename the folder:

```bash
git mv docs/guide docs/handbook
```

Then:

1. Update any `nav:` or `arrange:` references in `.pages` files.
2. Update internal links that point into the renamed folder. Find them:
   ```bash
   grep -rn "](../guide/" docs/ | grep -v "^docs/handbook/"
   grep -rn "](guide/" docs/
   ```
3. Add a redirect in `mkdocs.yml` to preserve external bookmarks:
   ```yaml
   plugins:
     - redirects:
         redirect_maps:
           'guide/index.md': 'handbook/index.md'
           'guide/installation.md': 'handbook/installation.md'
           # ...one per migrated page
   ```
4. Run `mkdocs build --strict` and fix anything it flags.

Rule of thumb: rename the label (A) freely; rename the URL (B) only when you really need to, and always with redirects.
