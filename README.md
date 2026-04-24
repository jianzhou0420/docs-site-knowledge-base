# docs-site-knowledge-base

**A scaffolding for building personal knowledge bases with Claude as the primary author.**

You drop source material — papers, article clippings, notes, code excerpts, experiment logs — into the repo. You ask Claude to organize, summarize, and cross-link it. The result is a browsable static site you can read locally, search, and share.

The repo pairs MkDocs Material with a filesystem-driven nav so Claude can shape the knowledge base by creating, moving, and editing markdown files — **no config YAML surgery required**. Claude reads the `docs/` tree, writes to it, and queries across it. You read the rendered site.

## Why this shape

| Requirement of an LLM-authored KB | How this repo answers it |
|---|---|
| Additions shouldn't require a central-config edit | `awesome-pages` reads nav from the filesystem. Claude creates a file → the page appears. |
| Reorganizing should be cheap | Moving a folder updates the nav automatically. No cross-reference sweep. |
| Content should stay portable markdown | Plain `.md` files throughout. No vault-specific wiki syntax. |
| The author (Claude) needs to know the rules | Conventions are documented inside the rendered site under the **Guide** tab, so Claude can read them on demand. |
| You want to *read* the result, not just diff it | MkDocs Material gives you a fast, searchable site with dark mode out of the box. |

Same spirit as Andrej Karpathy's "LLM Knowledge Bases" workflow (raw sources → LLM-compiled wiki → browsable frontend); different tools. Karpathy uses Obsidian as the IDE; this repo uses MkDocs as a static-site renderer, which trades the graph view for out-of-the-box publishability and search.

## What's in the repo

```
.
├── docs/
│   ├── guide/                        Install, quick-start, rationale, conventions
│   └── recipes/                      Task-oriented how-tos (add a page, add a tab, …)
├── mkdocs.yml                        MkDocs + Material + awesome-pages + redirects
├── requirements.txt                  Plugin dependencies
├── run_dev.sh                        `mkdocs serve -a 127.0.0.1:8001`
└── scripts/
    └── check_anchors.py              Post-renumbering anchor-drift fixer
```

The site that ships in `docs/` is **self-documenting** — it's both the manual for the scaffold and a live demonstration of what a filesystem-driven KB looks like. Replace its content with yours as your KB grows.

## Getting started

```bash
git clone https://github.com/jianzhou0420/docs-site-knowledge-base.git my-kb
cd my-kb
conda create -n my-kb python=3.11 -y
conda activate my-kb
pip install -r requirements.txt
./run_dev.sh
# → http://127.0.0.1:8001
```

Full install notes, the conventions your Claude agent should follow, and worked recipes live under the **Guide** and **Recipes** tabs of the rendered site. Rationale and tradeoffs are in `Guide → Why this pattern`.

## A typical session

1. Drop a source — a paper PDF, a clipping, a conversation transcript — into a topical folder under `docs/`.
2. Ask Claude to summarize it, extract concepts, and link it to existing pages.
3. Browse the result in the dev server. Move files around if the organization isn't right.
4. When the KB is big enough, query Claude across it ("what have I learned about X?") and file the answer back into `docs/` as a new synthesized page.

The human rarely writes the wiki directly. The human drops material, asks questions, and reads.

## License

MIT. See `LICENSE`.
