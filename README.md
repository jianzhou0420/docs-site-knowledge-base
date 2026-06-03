# docs-site-knowledge-base

**A scaffold for building personal knowledge bases with Claude as the primary author — rendered as a zero-dependency static HTML site.**

You drop source material — papers, article clippings, notes, code excerpts, experiment logs — into the repo. You ask Claude to organize, summarize, and cross-link it. The result is a browsable static site you can read locally and share.

The site is **pure HTML** with a tiny Python-standard-library engine that gives it filesystem-driven navigation. There is **no `pip`, no `npm`, no build step** — if you have `python3`, you can run it. Claude shapes the knowledge base by creating, moving, and editing HTML files; the engine turns the file tree into tabs, sidebars, breadcrumbs, and an on-this-page TOC.

## Why this shape

| Requirement of an LLM-authored KB | How this repo answers it |
|---|---|
| Additions shouldn't require a central-config edit | Nav is read from the filesystem. Claude creates `docs/pages/<tab>/<page>.html` → the page appears. |
| Reorganizing should be cheap | Moving a folder re-routes the nav. No central nav list to keep in sync. |
| Content should stay portable and durable | Plain `.html` files. No generator, no plugins, nothing to rot. It renders the same in three years. |
| The author (Claude) needs to know the rules | Conventions are documented inside the rendered site under the **Guide** tab, so Claude can read them on demand. |
| You want to *read* the result, not just diff it | A shared layout gives every page a header, sidebar, breadcrumbs, dark mode, and a right-hand TOC. |

Same spirit as Andrej Karpathy's "LLM Knowledge Bases" workflow (raw sources → LLM-compiled wiki → browsable frontend); different tools. This repo trades a generator's plugin ecosystem (search, diagrams, i18n) for radical simplicity and zero-dependency longevity.

## How it works

- **`docs/pages/<dir>/`** — each directory is a top tab; each `.html` file is a page. (`_lib/_nav.py` scans this tree.)
- **`docs/_lib/`** — the engine: a live-reload dev server, a shared HTML layout, the filesystem nav, and a wrap script.
- **Authoring** — you write a page as a normal HTML doc whose content sits in a `<main class="doc-body">` block. Running `python3 docs/_lib/_wrap_handwritten.py` bakes the current chrome (header / sidebar / breadcrumbs / TOC / footer) onto every page. It's idempotent.
- **`docs/_site.json`** — branding (site name, tagline, footer). **`docs/pages/<tab>/_tab.json`** — per-tab label, order, and sidebar grouping.

## What's in the repo

```
.
├── docs/
│   ├── index.html                    Root landing page
│   ├── _site.json                    Branding config (site name, tagline, footer)
│   ├── _lib/
│   │   ├── _serve.py                 Live-reload dev server (stdlib HTTP + SSE)
│   │   ├── _layout.py                Shared HTML layout shell
│   │   ├── _nav.py                   Filesystem-driven tabs + sidebar
│   │   ├── _wrap_handwritten.py      Bakes chrome onto authored pages
│   │   └── _site.py                  Loads _site.json
│   ├── assets/
│   │   ├── style.css                 Theme + layout styles
│   │   └── nav.js                    Theme toggle, mobile drawer, TOC scroll-spy
│   └── pages/
│       ├── guide/                    Install, quick-start, conventions, rationale
│       └── recipes/                  Task how-tos (add a page/tab, group the sidebar)
└── run_dev.sh                        ./run_dev.sh → http://0.0.0.0:8002
```

The site that ships in `docs/` is **self-documenting** — it's both the manual for the scaffold and a live demonstration of a filesystem-driven KB. Replace its content with yours as your KB grows.

## Getting started

```bash
git clone https://github.com/jianzhou0420/docs-site-knowledge-base.git my-kb
cd my-kb
./run_dev.sh
# → http://0.0.0.0:8002
```

No environment to create, no dependencies to install. Edit a page and the browser live-reloads. After adding, moving, or renaming pages, run `python3 docs/_lib/_wrap_handwritten.py` to refresh the chrome.

Full install notes, the conventions your Claude agent should follow, and worked recipes live under the **Guide** and **Recipes** tabs of the rendered site. Rationale and tradeoffs are in *Guide → Why this pattern*.

## A typical session

1. Drop a source — a paper PDF, a clipping, a conversation transcript — somewhere you can reach it.
2. Ask Claude to summarize it, extract concepts, write it up as an HTML page under `docs/pages/`, and link it to existing pages.
3. Claude runs the wrap script; you browse the result in the dev server. Move files around if the organization isn't right.
4. When the KB is big enough, query Claude across it ("what have I learned about X?") and file the answer back as a new synthesized page.

The human rarely writes the wiki directly. The human drops material, asks questions, and reads.

## License

MIT. See `LICENSE`.
