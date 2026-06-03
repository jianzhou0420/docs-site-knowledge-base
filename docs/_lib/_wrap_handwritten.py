#!/usr/bin/env python3
"""Re-wrap every doc-site HTML page with the current layout shell.

The site is HTML-first — each `<main>` block holds the authored content; the
chrome (top header, breadcrumbs, sidebar, right-TOC, footer) is regenerated
from `_layout.py` + `_nav.py`. Run this any time you change layout/nav and
want the new chrome propagated to all pages.

Targets:
  - docs/index.html              — root landing
  - docs/pages/**/*.html         — every doc page

For each page we:
  1. Read existing <title>, <main> inner content, and last-updated text
  2. Strip the layout-regenerated topbar from inside <main>
  3. Re-render via `_layout.render(meta, body, toc)` with auto-derived metadata
  4. Write back, idempotent (CONVERTED_MARKER guards against double-wrap)

A small HANDWRITTEN dict at the top supplies per-page overrides (e.g. spine
pages with custom section_class). Everything else gets metadata derived from
its path.
"""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

import _layout
import _nav
from _site import SITE_NAME

# docs/ root — script lives at docs/_lib/_wrap_handwritten.py.
V2 = Path(__file__).resolve().parent.parent

# Per-page overrides. Any field absent here is auto-derived. Keys are paths
# relative to docs/. Add an entry here only when a page needs chrome that
# can't be inferred from its path (e.g. the root landing has no sidebar
# section, so its right-TOC is suppressed). Everything else is automatic.
HANDWRITTEN: dict[str, dict] = {
    "index.html": {
        "section_class": "blueprint",
        "breadcrumbs": [(SITE_NAME, "")],
        "has_right_toc": False,
    },
}

# Per-section accent (CSS class names defined in assets/style.css). The first
# matching path-prefix wins, so list more-specific prefixes first. Unmatched
# pages fall back to "guide". Accents are purely cosmetic.
SECTION_CLASS_BY_PREFIX = (
    ("pages/recipes/", "designdoc"),
    ("pages/guide/", "guide"),
)

# Pretty labels for directory names that don't title-case cleanly. Most dirs
# render fine from auto title-casing ("getting-started" → "Getting Started");
# add a row only when that's wrong.
DIR_LABEL_OVERRIDES: dict[str, str] = {}

# Marker we drop into the file so we know we already converted it.
CONVERTED_MARKER = "<!-- site-layout -->"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.IGNORECASE)
STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
BODY_RE = re.compile(r"<body[^>]*>(.*?)</body>", re.DOTALL | re.IGNORECASE)
MAIN_RE = re.compile(r'<main\s+class="doc-body[^"]*"[^>]*>(.*?)</main>', re.DOTALL | re.IGNORECASE)
LAST_UPDATED_RE = re.compile(r'<div class="last-updated">(.*?)</div>', re.DOTALL | re.IGNORECASE)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
H2_ID_RE = re.compile(r'<h([23])[^>]*\bid="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL | re.IGNORECASE)


def _dir_label(name: str) -> str:
    return DIR_LABEL_OVERRIDES.get(name, name.replace("-", " ").replace("_", " ").title())


def _strip_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _tab_for(rel: str) -> str:
    """Active tab label for a page at `rel` (path relative to docs/).

    Tabs are scanned from docs/pages/<dir>/ (see _nav.get_tabs), so this
    is plug-and-play — no hardcoded tab names. Pages outside pages/
    (e.g. the root index.html) fall back to the first discovered tab."""
    tabs = _nav.get_tabs()
    if not tabs:
        return SITE_NAME
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] == "pages":
        for t in tabs:
            if t.get("_dir") == parts[1]:
                return t["tab"]
    return tabs[0]["tab"]


def _section_class_for(rel: str) -> str:
    for prefix, cls in SECTION_CLASS_BY_PREFIX:
        if rel.startswith(prefix):
            return cls
    return "guide"


def _auto_breadcrumbs(rel: str, title: str) -> list:
    """Derive page-relative breadcrumbs from the docs-relative page path."""
    if rel == "index.html":
        return [(SITE_NAME, "")]
    parts = rel.split("/")
    output_dir = (V2 / rel).parent

    def relhref(target_abs: Path) -> str:
        return os.path.relpath(target_abs, output_dir)

    crumbs: list = [(SITE_NAME, relhref(V2 / "index.html"))]
    accum: list[str] = []
    for seg in parts[:-1]:
        accum.append(seg)
        idx_abs = V2 / "/".join(accum) / "index.html"
        href = relhref(idx_abs) if idx_abs.exists() else ""
        crumbs.append((_dir_label(seg), href))
    if parts[-1] == "index.html":
        # Section landing — mark the last existing crumb as self (empty href)
        if crumbs:
            crumbs[-1] = (crumbs[-1][0], "")
    else:
        crumbs.append((title, ""))
    return crumbs


def _toc_from_body(body_html: str) -> list:
    """Build (level, anchor, text) tuples from <h2 id=...> and <h3 id=...> in body."""
    entries = []
    for m in H2_ID_RE.finditer(body_html):
        level = int(m.group(1))
        anchor = m.group(2)
        text = _strip_html_tags(m.group(3))
        entries.append((level, anchor, text))
    return entries


def convert(path: Path) -> bool:
    rel = path.relative_to(V2).as_posix()
    raw = path.read_text(encoding="utf-8")
    already_wrapped = CONVERTED_MARKER in raw

    # Pull title
    m = TITLE_RE.search(raw)
    title = m.group(1).strip() if m else path.stem
    title_suffix = f" — {SITE_NAME}"
    if title_suffix in title:
        title = title.split(title_suffix, 1)[0].strip()
    # Fully unescape so the eventual html.escape at render time produces exactly
    # one layer (idempotent). Without this loop, each re-wrap pass doubles every
    # `&amp;` (e.g. "&amp;" → "&amp;amp;"), and titles with `&` grow unbounded.
    prev = None
    while title != prev:
        prev = title
        title = html.unescape(title)

    # Pull style blocks from head only
    head_end = raw.lower().find("</head>")
    head_part = raw[:head_end] if head_end != -1 else ""
    styles = STYLE_RE.findall(head_part)
    extra_head = "\n".join(styles)

    # Extract last_updated from topbar (before stripping it)
    last_updated = ""
    m_lu = LAST_UPDATED_RE.search(raw)
    if m_lu:
        last_updated = _strip_html_tags(m_lu.group(1)).strip()

    # Pick content body — always prefer the innermost <main class="doc-body">,
    # which preserves authored content across layout changes. The CONVERTED_MARKER
    # check is now informational; we rely on the presence of <main>, not the marker.
    main_matches = list(MAIN_RE.finditer(raw))
    if main_matches:
        # Innermost match: take the last one (handles accidentally double-wrapped pages).
        body_inner = main_matches[-1].group(1)
    else:
        m = BODY_RE.search(raw)
        if not m:
            print(f"  SKIP (no <body> and no <main>): {rel}")
            return False
        body_inner = m.group(1)
    _ = already_wrapped  # silence unused-variable lint

    # Pull and remove trailing <script> blocks (preserve them)
    inline_scripts = SCRIPT_RE.findall(body_inner)
    body_inner = SCRIPT_RE.sub("", body_inner)
    extra_body_end = "\n".join(inline_scripts)

    # Strip layout-regenerated topbar
    body_inner = re.sub(
        r'<div class="topbar">\s*<div class="crumbs">.*?</div>\s*(?:<div class="last-updated">.*?</div>\s*)?</div>',
        "",
        body_inner,
        count=1,
        flags=re.DOTALL,
    )
    # Strip the layout-regenerated footer (single <span> inside <footer>) that a
    # prior wrap pass baked into body_inner — otherwise each re-wrap stacks another.
    # Structural match so it keeps working when site_name (and thus the footer
    # text) changes between passes.
    body_inner = re.sub(
        r"<footer>\s*<span>[^<]*</span>\s*</footer>",
        "",
        body_inner,
        flags=re.IGNORECASE,
    )
    body_inner = body_inner.strip()

    # Prefer the body's <h1> as the authoritative page title: it never carries the
    # " — <site>" suffix, so it survives a site rename cleanly (deriving the title
    # only from the existing <title> would re-append the new suffix and leave the
    # old name stranded — "Guide — Old — New"). Fall back to the <title> otherwise.
    m_h1 = H1_RE.search(body_inner)
    if m_h1:
        h1_text = html.unescape(_strip_html_tags(m_h1.group(1)))
        if h1_text:
            title = h1_text

    # Auto-derive overridable fields, then layer HANDWRITTEN overrides on top
    overrides = HANDWRITTEN.get(rel, {})
    tab = overrides.get("tab", _tab_for(rel))
    section_class = overrides.get("section_class", _section_class_for(rel))
    breadcrumbs = overrides.get("breadcrumbs", _auto_breadcrumbs(rel, title))
    has_right_toc = overrides.get("has_right_toc", True)

    toc = _toc_from_body(body_inner)

    meta = _layout.PageMeta(
        tab=tab,
        page_rel=rel,
        # Append the site-name suffix, except when the page title already IS the
        # site name (the root landing) — avoids a redundant "Foo — Foo" tab title.
        browser_title=html.escape(title) + (f" — {SITE_NAME}" if title != SITE_NAME else ""),
        section_class=section_class,
        breadcrumbs=breadcrumbs,
        last_updated=last_updated,
        has_right_toc=has_right_toc,
        extra_head=extra_head,
        extra_body_end=extra_body_end,
    )

    output = _layout.render(meta, body_inner, toc)
    output = output.replace("</head>", f"{CONVERTED_MARKER}\n</head>", 1)
    path.write_text(output, encoding="utf-8")
    return True


def discover_all_pages() -> list[Path]:
    """All .html files under docs/ that should be re-wrapped.

    Skips tab dirs marked `external_layout: true` in their `_tab.json` —
    those pages own their chrome and the wrapper would mangle them.
    """
    pages: list[Path] = []
    root_index = V2 / "index.html"
    if root_index.exists():
        pages.append(root_index)
    pages_dir = V2 / "pages"
    if not pages_dir.exists():
        return pages
    external_dirs = {t["_dir"] for t in _nav.get_tabs() if t.get("external_layout")}
    for f in sorted(pages_dir.rglob("*.html")):
        rel = f.relative_to(V2)
        # rel.parts[0] == "pages"; parts[1] is the tab dir
        if len(rel.parts) >= 2 and rel.parts[1] in external_dirs:
            continue
        pages.append(f)
    return pages


def main():
    n_ok = 0
    n_skip = 0
    for path in discover_all_pages():
        try:
            if convert(path):
                n_ok += 1
            else:
                n_skip += 1
        except Exception as e:
            print(f"  ERROR {path.relative_to(V2)}: {type(e).__name__}: {e}")
            n_skip += 1
    print(f"\ndone — {n_ok} re-wrapped, {n_skip} skipped/error")


if __name__ == "__main__":
    main()
