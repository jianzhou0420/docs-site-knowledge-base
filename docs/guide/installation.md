# Installation

## Prerequisites

- Python 3.9 or newer.
- Git (for cloning; not strictly required if you download a ZIP, but strongly recommended for version control of your own content).

## Clone

```bash
git clone https://github.com/jianzhou0420/docs-site-knowledge-base.git my-docs
cd my-docs
```

Or use the "Use this template" button on GitHub to create your own repo from this one.

## Install dependencies

Create a virtualenv (optional but recommended) and install the plugins.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` pins the minimum versions:

| Package | Purpose |
|---|---|
| `mkdocs` | Core static site generator |
| `mkdocs-material` | Theme |
| `mkdocs-awesome-pages-plugin` | Filesystem-driven nav |
| `mkdocs-redirects` | Root `/` redirect |
| `mkdocs-glightbox` | Optional image lightbox |

## Serve locally

```bash
./run_dev.sh
```

Equivalent to `mkdocs serve -a 127.0.0.1:8001`. Live-reloads on file changes. Open [http://127.0.0.1:8001](http://127.0.0.1:8001) — the site will redirect you to this very page's sibling, `/guide/index.html`.

## Build a static site

```bash
mkdocs build            # writes ./site/
mkdocs build --strict   # same, but treat warnings as errors (recommended for CI)
```

## Uninstall

Delete the clone. No system-wide state is created.

## Troubleshooting

- **"Plugin 'awesome-pages' not installed"** — run `pip install -r requirements.txt` in the active environment.
- **`mkdocs build --strict` fails on anchor warnings** — run `python scripts/check_anchors.py` to see proposed fixes; `--apply` to rewrite source files. See [Conventions §9](conventions.md#9-anchor-links-beware-slug-drift).
- **`/` loads nothing** — the redirect target in `mkdocs.yml` (`redirects.redirect_maps`) must point to a real page. Default is `guide/index.md`.
