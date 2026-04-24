# docs-site-knowledge-base

A self-documenting starter for **MkDocs Material** doc-sites where **the filesystem is the nav** — drop a folder, it becomes a tab; drop a file, it becomes a page. No `mkdocs.yml` edits when adding content.

This repo *is* an example of the pattern it teaches: the full guide, rationale, and recipes live in `docs/` and render as a browsable doc-site. Run `./run_dev.sh` after install to read it.

## Getting started

```bash
git clone https://github.com/jianzhou0420/docs-site-knowledge-base.git my-docs
cd my-docs
pip install -r requirements.txt
./run_dev.sh
# → http://127.0.0.1:8001
```

Full installation notes, rationale, conventions, and recipes are in the rendered docs under the **Guide** and **Recipes** tabs.

## Repo layout

```
.
├── mkdocs.yml                        Material theme + awesome-pages + redirects
├── requirements.txt                  Plugin deps
├── run_dev.sh                        `mkdocs serve -a 127.0.0.1:8001`
├── scripts/
│   └── check_anchors.py              Broken-anchor reporter / auto-fixer
└── docs/
    ├── guide/                        Install, quick-start, rationale, conventions
    ├── recipes/                      Task-oriented how-tos
    └── stylesheets/extra.css         CSS — ignored by nav, still served
```

## License

MIT. See `LICENSE`.
