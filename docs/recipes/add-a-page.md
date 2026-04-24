# Add a page

## Minimum steps

```bash
touch docs/guide/new-page.md
echo "# New page" > docs/guide/new-page.md
```

Refresh the dev server. The page appears in the **Guide** sidebar. No other changes needed.

## Controlling position

By default, new pages appear in alphabetical order. To place it in a specific slot, edit that folder's `.pages`:

```yaml
nav:
  - index.md
  - Installation: installation.md
  - New page: new-page.md        # ← inserted here
  - Quick Start: quick-start.md
```

## Giving it a friendly title

The sidebar label defaults to the first `# Heading` in the file. Override in `.pages`:

```yaml
- "A Very Custom Title": new-page.md
```

## Linking to it

From another page in the same folder:

```markdown
[New page](new-page.md)
```

From a different folder:

```markdown
[New page](../guide/new-page.md)
```

Always use `.md` extensions in links — MkDocs handles the extension-to-URL translation.
