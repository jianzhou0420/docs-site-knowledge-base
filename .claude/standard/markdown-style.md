# Markdown Style

Rules for all markdown files in `docs/` (the rendered knowledge base).

## Structure

1. **Title (H1)** — one per file.
2. **`last updated:` line** — required on every file, right after the H1 title. Get the exact time via `date '+%Y-%m-%d %H:%M'`.
3. **Intro paragraph** — 1–3 sentences framing what the page is about.
4. **Table of Contents** — for pages with 4+ numbered sections, add an inline TOC after the intro with anchor links.
5. **Numbered sections** — `## 1. Section Name` for top-level sections, `### 1.1 Subsection` for subsections. Numbering is optional for short pages (< 3 sections).
6. **Changelog** — every substantive page ends with a `## Changelog` section.

## Example

```markdown
# Page Title

last updated: 2026-04-24 15:30

---

Brief intro paragraph.

## Table of Contents

1. [What is X?](#1-what-is-x)
2. [How it works](#2-how-it-works)
3. [When to use it](#3-when-to-use-it)

---

## 1. What is X?

Content...

### 1.1 Background

Content...

## 2. How it works

Content...

## 3. When to use it

Content...

---

## Changelog

- 2026-04-24 15:30: Initial content
```

## Paper / source references

Every mention of a paper or named method should be a **clickable link with a date**:

| Context | Format | Example |
|---------|--------|---------|
| Tables | `[**Name**](url) (YY.MM)` | `[**AFlow**](https://arxiv.org/abs/2410.10762) (24.10)` |
| Inline | `[Name](url) (YY.MM)` | `inspired by [AFlow](https://arxiv.org/abs/2410.10762) (24.10)` |
| Block intro | `[**Name**](url) (YY.MM): …` | `[**AFlow**](https://arxiv.org/abs/2410.10762) (24.10): MCTS over…` |

- **Date format**: `(YY.MM)` — for arXiv papers, derived from the v1 submission date.
- **Always link**: no unlinked `**Name**` references.
- **Date placement**: outside the link syntax — `[text](url) (YY.MM)`, not `[text (YY.MM)](url)`.

## Formatting

- **Tables** for structured comparisons — beats paragraph prose for side-by-side content.
- **Code blocks** with language tags for examples.
- **Collapsed admonitions** `??? info "Sources"` for reference lists inside sections.
- **Bold** for key terms on first use, then plain.
- **Relative links** — always use `[text](../other-folder/file.md)` (with `.md`) rather than absolute URLs for internal references; MkDocs handles the extension translation.

## Slug drift

Section headings like `## 1. Canvas & Editor` slugify to `#1-canvas-editor` (ampersands and multiple spaces collapse to single dashes). When you write same-page anchor links `[something](#1-canvas-editor)`, use the collapsed form — MkDocs strict builds will flag mismatches.

The template ships a helper at `scripts/check_anchors.py` that parses MkDocs' warnings, matches broken anchors against real IDs in the built HTML, and proposes replacements (`--apply` rewrites the source).
