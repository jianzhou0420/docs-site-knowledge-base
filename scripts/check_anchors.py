#!/usr/bin/env python3
"""Report broken same-page anchor links and suggest fixes.

MkDocs emits INFO-level warnings for broken #anchor fragments; this script
parses them, reads the built site to discover the real anchor IDs, and
proposes per-file replacements. Useful after section renumbering or slug
drift.

Usage:
    python scripts/check_anchors.py            # analyze only, print report
    python scripts/check_anchors.py --apply    # apply fixes to source .md

Notes:
- Run `mkdocs build` at least once first so site/ is populated.
- Heuristics: exact match -> double-dash collapse -> fuzzy (difflib, 0.5).
- `--apply` performs plain string replacement. Distinctive anchor strings
  (containing section numbers / ADR tags) are safe; short / generic
  anchors may need manual review before applying.
"""
import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys


DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


def md_to_html_path(md_rel: str) -> pathlib.Path:
    p = md_rel
    if p.endswith("/index.md"):
        p = p[: -len("index.md")]
    elif p.endswith(".md"):
        p = p[:-3] + "/"
    return SITE / p / "index.html"


def anchors_in(html_path: pathlib.Path) -> list[str]:
    if not html_path.exists():
        return []
    return re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', html_path.read_text())


def collect_broken() -> list[tuple[str, str]]:
    log = subprocess.run(
        ["mkdocs", "build"],
        cwd=DOCS.parent,
        capture_output=True,
        text=True,
    ).stderr
    return re.findall(
        r"Doc file '([^']+)' contains a link '(#[^']+)', "
        r"but there is no such anchor on this page\.",
        log,
    )


def suggest_fixes(broken: list[tuple[str, str]]) -> dict[str, list[tuple[str, str]]]:
    by_file: dict[str, list[str]] = {}
    for f, a in broken:
        by_file.setdefault(f, []).append(a)

    fixes: dict[str, list[tuple[str, str]]] = {}
    for md_rel, bad_anchors in by_file.items():
        ids = anchors_in(md_to_html_path(md_rel))
        if not ids:
            continue
        for bad in bad_anchors:
            key = bad.lstrip("#")
            collapsed = key.replace("--", "-")
            if collapsed in ids:
                cand = collapsed
            else:
                close = difflib.get_close_matches(key, ids, n=1, cutoff=0.5)
                cand = close[0] if close else None
            if cand and cand != key:
                fixes.setdefault(md_rel, []).append((bad, f"#{cand}"))
    return fixes


def apply_fixes(fixes: dict[str, list[tuple[str, str]]]) -> None:
    for rel, pairs in fixes.items():
        p = DOCS / rel
        txt = p.read_text()
        for bad, good in pairs:
            txt = txt.replace(bad, good)
        p.write_text(txt)
        print(f"patched {rel}: {len(pairs)} anchor(s)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="rewrite source .md files")
    parser.add_argument("--json", action="store_true", help="emit fixes as JSON")
    args = parser.parse_args()

    broken = collect_broken()
    fixes = suggest_fixes(broken)

    if args.json:
        print(json.dumps(fixes, indent=2))
    else:
        print(f"Broken anchors: {len(broken)}")
        for rel, pairs in fixes.items():
            print(f"\n{rel}")
            for bad, good in pairs:
                print(f"  {bad} -> {good}")

    if args.apply:
        apply_fixes(fixes)
        print(f"\nApplied fixes to {len(fixes)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
