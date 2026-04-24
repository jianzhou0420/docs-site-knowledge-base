# Virtual sub-sections

Sometimes a folder has 20+ flat files and you want them grouped thematically in the sidebar — without creating sub-folders.

This is **virtual grouping**: the grouping exists in `.pages`, not in the filesystem.

## Example

Filesystem (flat):

```
docs/knowledge-base/
├── index.md
├── bench-vln.md
├── bench-eqa.md
├── bench-vla.md
├── method-navgpt.md
├── method-mapgpt.md
└── method-smartway.md
```

`.pages` with virtual groups:

```yaml
title: Knowledge Base
nav:
  - index.md
  - Benchmarks:
    - "VLN": bench-vln.md
    - "EQA": bench-eqa.md
    - "VLA": bench-vla.md
  - Methods:
    - "NavGPT": method-navgpt.md
    - "MapGPT": method-mapgpt.md
    - "SmartWay": method-smartway.md
```

Rendered sidebar:

```
Knowledge Base
├── Benchmarks
│   ├── VLN
│   ├── EQA
│   └── VLA
└── Methods
    ├── NavGPT
    ├── MapGPT
    └── SmartWay
```

## Why this instead of sub-folders?

- **Fewer rename cascades.** Moving a file between groups is one edit in `.pages`; no git-mv, no link rewrites.
- **One-level-deep URLs** stay short: `/knowledge-base/method-navgpt/` reads better than `/knowledge-base/methods/navgpt/`.
- **Nav and filesystem can evolve independently.** Regroup for readability without touching content.

## When to use real sub-folders instead

- When the sub-group is conceptually a separate *unit* that may be extracted, linked to, or searched in isolation (e.g. `claude-code/` as a whole — its files are tightly related and it's a self-contained study).
- When the sub-group has 20+ files of its own (flatness gets cluttered past a point).

## Mixing

You can mix: some groups in `.pages` are virtual (files), others are folder references:

```yaml
title: Knowledge Base
nav:
  - index.md
  - Benchmarks:
    - bench-vln.md
    - bench-eqa.md
  - Methods:               # virtual group of flat files
    - method-navgpt.md
    - method-mapgpt.md
  - Claude Code Study: claude-code     # real sub-folder, has its own .pages
```

Both work.
