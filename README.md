# docsite-starter

A starter repo for **MkDocs Material** doc-sites where **the filesystem is the nav** — drop a folder, it becomes a tab; drop a file, it becomes a page. No `mkdocs.yml` edits when adding content.

Distilled from a real project's migration. See `CONVENTIONS.md` for the rules.

## What's in here

```
.
├── mkdocs.yml                        Material theme + awesome-pages + redirects
├── requirements.txt                  Minimal plugin set
├── run_dev.sh                        `mkdocs serve` launcher
├── CONVENTIONS.md                    How to use this pattern — read first
├── scripts/
│   └── check_anchors.py              Broken-anchor reporter / auto-fixer
└── docs/
    ├── developer-guide/              Example tab
    ├── research/                     Example tab (with HTML deck pattern)
    ├── knowledge-base/               Example tab (with virtual sub-sections)
    └── stylesheets/                  CSS — ignored by nav, still served
```

## Why this pattern

Traditional MkDocs sites maintain an explicit `nav:` tree in `mkdocs.yml`. Every new page means two edits: add the file, update the nav. When the nav gets long (100+ pages), the config file turns into a maintenance tax.

This template removes that tax:

- **`awesome-pages`** drives the nav from the filesystem. Folders = sections, files = pages, order can be customised with a per-folder `.pages` file when alphabetical isn't right.
- **`mkdocs-redirects`** sends `/` to a canonical landing page so the root doesn't need a dedicated `index.md` that duplicates the nav.
- **Per-folder `.pages`** files let you override titles or group flat files into virtual sub-sections without sub-directories.

Result: most additions are zero-config. Reorganising means moving folders, not editing config.

## Getting started

```bash
# 1. Clone (or use as a GitHub template)
git clone <this-repo> my-project-docs
cd my-project-docs

# 2. Install
pip install -r requirements.txt

# 3. Serve locally
./run_dev.sh
# → http://127.0.0.1:8001

# 4. Edit
#    - Replace site_name in mkdocs.yml
#    - Replace docs/developer-guide/core/blueprint.md with your content
#    - Add folders and files; they auto-surface
#    - Read CONVENTIONS.md for the rules
```

## Deploy

Not wired in — too host-dependent. Hooks worth considering:

- **GitHub Pages**: add `.github/workflows/deploy.yml` with `mkdocs gh-deploy --force` on push to `main`.
- **Netlify / Cloudflare Pages**: point at the repo, build command `mkdocs build`, publish dir `site`.
- **Self-hosted**: `mkdocs build` → serve `site/` from any static host.

## When NOT to use this template

- **Tiny sites** (< 10 pages) — an explicit `nav:` is fine and simpler for readers of your config.
- **Heavy multi-lingual** (i18n) — `awesome-pages` doesn't model i18n; consider `mkdocs-static-i18n` patterns instead.
- **Strict audit / compliance** where the nav must be reviewed as a single artefact — explicit nav gives a single diff point.

## License

MIT. See `LICENSE`.

---

**Next read**: [`CONVENTIONS.md`](CONVENTIONS.md) — the operating rules.
