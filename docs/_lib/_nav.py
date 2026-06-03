#!/usr/bin/env python3
"""Site navigation for docs/ — plug-and-play, filesystem-driven.

Each top tab is discovered by scanning `docs/pages/<dir>/`. Drop a new
directory in → new tab appears. Delete it → tab disappears. Code in
this file has zero awareness of any specific tab's existence (no
"Research" / "AAS" / etc. strings hardcoded).

Per-tab overrides live in `docs/pages/<dir>/_tab.json`. Fields (all
optional):

  label             str    — tab text (default: title-cased dir name)
  key               str    — CSS accent class (default: dir name)
  landing           str    — landing path *relative to the tab dir*
                              (default: "index.html"; falls back to
                               the first index.html found anywhere
                               under the dir)
  order_priority    int    — smaller = leftward in the tab strip
                              (default: 100; ties broken by dir name)
  external_layout   bool   — page has its own chrome; wrapper skips it
                              (default: false)
  sections          list   — curated sidebar groups. Each entry:
      label    : section label
      dir      : path relative to the tab dir (or to docs/ root if
                  it already starts with "pages/")
      key      : CSS accent class
      order    : optional curated stem order inside that section
      files_only / depth_limit : same semantics as before

  Without `sections`, the sidebar auto-discovers from the tab dir —
  each subdir becomes a section, alphabetical.
"""

from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from _site import SITE_NAME

# Resolves to the docs/ root (script lives at docs/_lib/_nav.py).
V2 = Path(__file__).resolve().parent.parent
PAGES = V2 / "pages"


# ---------- per-tab config loading ----------


def _default_label(dir_name: str) -> str:
    return dir_name.replace("-", " ").replace("_", " ").title()


def _load_tab_cfg(tab_dir: Path) -> dict:
    cfg_file = tab_dir / "_tab.json"
    if not cfg_file.exists():
        return {}
    try:
        return json.loads(cfg_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"warn: bad _tab.json at {cfg_file}: {e}")
        return {}


def _find_default_landing(tab_dir: Path) -> str | None:
    """Pick a landing path (relative to tab_dir). Prefer tab_dir/index.html;
    else first index.html found anywhere underneath."""
    direct = tab_dir / "index.html"
    if direct.exists():
        return "index.html"
    for f in sorted(tab_dir.rglob("index.html")):
        return f.relative_to(tab_dir).as_posix()
    return None


def get_tabs() -> list[dict]:
    """Scan docs/pages/<dir>/ and return one tab dict per discovered dir.

    Returns same shape as the old hardcoded TABS list, with one extra
    `_dir` field so consumers can find a tab by directory name.
    """
    if not PAGES.exists():
        return []

    discovered: list[tuple[tuple, dict]] = []
    for d in sorted(PAGES.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
            continue
        cfg = _load_tab_cfg(d)
        landing_rel = cfg.get("landing") or _find_default_landing(d)
        if landing_rel is None:
            # Nothing serveable in this dir — skip silently (matches
            # the user-facing contract: "tab disappears if absent").
            continue
        landing = f"pages/{d.name}/{landing_rel}"

        label = cfg.get("label") or _default_label(d.name)
        key = cfg.get("key") or d.name
        external = bool(cfg.get("external_layout"))
        priority = int(cfg.get("order_priority", 100))

        sections_cfg = cfg.get("sections")
        if sections_cfg is None:
            # Default: one auto-discovered section per subdir under the
            # tab dir. (If there are no subdirs, the section list is
            # empty and render_sidebar will silently skip rendering.)
            sections_cfg = []
            for sub in sorted(d.iterdir()):
                if sub.is_dir() and not sub.name.startswith("_") and not sub.name.startswith("."):
                    sections_cfg.append(
                        {"label": _default_label(sub.name), "dir": sub.name, "key": key}
                    )

        # Resolve each section's `dir` to be relative to docs/ root.
        sections: list[dict] = []
        for sec in sections_cfg:
            sec = dict(sec)
            sec_dir = sec.get("dir", "")
            if not sec_dir.startswith("pages/"):
                sec["dir"] = f"pages/{d.name}/{sec_dir}".rstrip("/")
            sections.append(sec)

        discovered.append(
            (
                (priority, d.name),
                {
                    "tab": label,
                    "key": key,
                    "landing": landing,
                    "sections": sections,
                    "external_layout": external,
                    "_dir": d.name,
                },
            )
        )

    discovered.sort(key=lambda t: t[0])
    return [t[1] for t in discovered]


# Eagerly evaluated for legacy consumers. Plug-and-play callers should
# prefer get_tabs() so the scan reruns each time.
TABS = get_tabs()


# ---------- title extraction ----------


class _TitleGrabber(HTMLParser):
    """Capture the <title> and the first <h1> from a page."""

    def __init__(self):
        super().__init__()
        self._in_title = False
        self._in_h1 = False
        self.title = ""
        self.h1 = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title" and not self.title:
            self._in_title = True
        elif tag == "h1" and not self.h1:
            self._in_h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1:
            self.h1 += data


def _page_title(html_path: Path) -> str:
    try:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return html_path.stem
    g = _TitleGrabber()
    g.feed(text)
    # Prefer the body's <h1>: it carries no " — <site>" suffix, so labels stay
    # correct after a site rename. Fall back to <title> with the suffix trimmed.
    title = g.h1.strip()
    if not title:
        title = g.title.strip()
        title = re.split(rf"\s+[—|·-]\s+{re.escape(SITE_NAME)}", title, maxsplit=1)[0].strip()
    # HTMLParser only decodes one layer of entities. Loop to be safe against
    # titles that recycled through `html.escape` multiple times.
    prev = None
    while title != prev:
        prev = title
        title = html.unescape(title)
    return html.escape(title) if title else html_path.stem


# ---------- discovery ----------

_DISCOVER_CACHE: dict[str, list[dict]] = {}


def _scan_dir(current: Path) -> list[dict]:
    """Recursive directory scan. index.html is consumed by the caller (it
    becomes the parent group's label/href), so this returns siblings + subdirs.
    """
    nodes: list[dict] = []
    files = sorted(
        [f for f in current.glob("*.html") if f.name != "index.html"],
        key=lambda p: p.stem.lower(),
    )
    for f in files:
        nodes.append(
            {
                "kind": "page",
                "label": _page_title(f),
                "href": f.relative_to(V2).as_posix(),
            }
        )
    for d in sorted([d for d in current.iterdir() if d.is_dir()]):
        idx = d / "index.html"
        if idx.exists():
            label = _page_title(idx)
            href = idx.relative_to(V2).as_posix()
        else:
            label = d.name.replace("-", " ").replace("_", " ").title()
            href = None
        nodes.append(
            {
                "kind": "group",
                "label": label,
                "href": href,
                "children": _scan_dir(d),
            }
        )
    return nodes


def _discover_tree(section: dict) -> list[dict]:
    """Return ordered tree nodes for a section's nav."""
    cache_key = "|".join(
        [
            section["dir"],
            "files_only" if section.get("files_only") else "",
            f"depth={section['depth_limit']}" if section.get("depth_limit") else "",
            f"order={','.join(section['order'])}" if section.get("order") else "",
        ]
    )
    if cache_key in _DISCOVER_CACHE:
        return _DISCOVER_CACHE[cache_key]

    base = V2 / section["dir"]
    if not base.exists():
        _DISCOVER_CACHE[cache_key] = []
        return []

    files_only = section.get("files_only", False)
    depth_limit = section.get("depth_limit")
    curated_order: list[str] = section.get("order") or []
    order_index = {stem: i for i, stem in enumerate(curated_order)}

    def _top_sort_key(p: Path) -> tuple:
        if p.name == "index.html":
            return (0, 0, "")
        if p.stem in order_index:
            return (1, order_index[p.stem], "")
        return (2, 0, p.stem.lower())

    top_files = sorted(base.glob("*.html"), key=_top_sort_key)
    nodes: list[dict] = [
        {"kind": "page", "label": _page_title(f), "href": f.relative_to(V2).as_posix()}
        for f in top_files
    ]

    if files_only:
        _DISCOVER_CACHE[cache_key] = nodes
        return nodes

    if depth_limit == 2:
        for d in sorted([d for d in base.iterdir() if d.is_dir()]):
            idx = d / "index.html"
            if idx.exists():
                nodes.append(
                    {
                        "kind": "page",
                        "label": _page_title(idx),
                        "href": idx.relative_to(V2).as_posix(),
                    }
                )
        _DISCOVER_CACHE[cache_key] = nodes
        return nodes

    for d in sorted([d for d in base.iterdir() if d.is_dir()]):
        idx = d / "index.html"
        if idx.exists():
            label = _page_title(idx)
            href = idx.relative_to(V2).as_posix()
        else:
            label = d.name.replace("-", " ").replace("_", " ").title()
            href = None
        nodes.append(
            {
                "kind": "group",
                "label": label,
                "href": href,
                "children": _scan_dir(d),
            }
        )
    _DISCOVER_CACHE[cache_key] = nodes
    return nodes


def _contains_active(nodes: list[dict], page_rel: str) -> bool:
    for n in nodes:
        if n["kind"] == "page":
            if n["href"] == page_rel:
                return True
        else:
            if n.get("href") == page_rel or _contains_active(n["children"], page_rel):
                return True
    return False


# ---------- rendering ----------


def render_top_header(active_tab: str, page_rel: str) -> str:
    """Render the sticky top header — logo, tabs, search button, theme toggle."""
    depth = page_rel.count("/")
    prefix = "../" * depth if depth else ""

    tabs_html = []
    for tab in get_tabs():
        is_active = tab["tab"] == active_tab
        href = prefix + tab["landing"]
        cls = "tab active" if is_active else "tab"
        tabs_html.append(f'<a class="{cls}" href="{href}">{html.escape(tab["tab"])}</a>')
    tabs_block = "\n        ".join(tabs_html)

    return f"""<header class="site-header">
  <div class="site-header-inner">
    <a class="site-logo" href="{prefix}index.html">{html.escape(SITE_NAME)}</a>
    <nav class="site-tabs">
        {tabs_block}
    </nav>
    <div class="site-actions">
      <button class="site-action search-btn" aria-label="Search" title="Search (coming)">🔍</button>
      <button class="site-action theme-toggle" aria-label="Toggle theme" title="Toggle dark mode">🌙</button>
      <button class="site-action mobile-nav-toggle" aria-label="Menu" title="Menu">☰</button>
    </div>
  </div>
</header>"""


def _render_nodes(nodes: list[dict], page_rel: str, prefix: str) -> str:
    parts: list[str] = []
    for n in nodes:
        if n["kind"] == "page":
            cls = "sb-page active" if n["href"] == page_rel else "sb-page"
            parts.append(f'<a class="{cls}" href="{prefix}{n["href"]}">{n["label"]}</a>')
            continue
        href = n.get("href")
        self_active = href == page_rel
        child_active = _contains_active(n["children"], page_rel)
        open_attr = " open" if (self_active or child_active) else ""
        if href:
            link_cls = "sb-group-link active" if self_active else "sb-group-link"
            label_html = f'<a class="{link_cls}" href="{prefix}{href}">{n["label"]}</a>'
        else:
            label_html = f'<span class="sb-group-label-text">{n["label"]}</span>'
        children_html = _render_nodes(n["children"], page_rel, prefix)
        parts.append(
            f'<details class="sb-subsection"{open_attr}>'
            f'<summary class="sb-subsection-label">{label_html}</summary>'
            f'<div class="sb-pages">{children_html}</div>'
            f"</details>"
        )
    return "\n      ".join(parts)


def render_sidebar(active_tab: str, page_rel: str) -> str:
    tabs = get_tabs()
    tab = next((t for t in tabs if t["tab"] == active_tab), tabs[0] if tabs else None)
    if tab is None:
        return '<aside class="sidebar-left" aria-label="Section navigation"></aside>'
    depth = page_rel.count("/")
    prefix = "../" * depth if depth else ""

    section_html = []
    for sec in tab["sections"]:
        nodes = _discover_tree(sec)
        if not nodes:
            continue
        contains_active = _contains_active(nodes, page_rel)
        open_attr = " open" if contains_active else ""
        body = _render_nodes(nodes, page_rel, prefix)
        section_html.append(
            f'<details class="sb-section"{open_attr}>'
            f'<summary class="sb-section-label">{sec["label"]}</summary>'
            f'<div class="sb-pages">{body}</div>'
            f"</details>"
        )
    sections_block = "\n  ".join(section_html)

    return f"""<aside class="sidebar-left" aria-label="Section navigation">
  <div class="sidebar-inner">
  {sections_block}
  </div>
</aside>"""


def asset_prefix(page_rel: str) -> str:
    depth = page_rel.count("/")
    return "../" * depth if depth else ""
