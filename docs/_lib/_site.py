#!/usr/bin/env python3
"""Site-wide branding config for docs/.

Single source of truth for the strings that used to be hardcoded into the
layout/nav code (site name, tagline, footer, logo target). Reads
`docs/_site.json` once at import; missing keys fall back to safe template
defaults so the site still renders if the file is absent or partial.

Consumers:
  _nav.py     — logo text, <title>-suffix trim regex
  _layout.py  — <title> suffix, footer text
  _wrap_handwritten.py — breadcrumb root, <title> suffix, footer-strip regex
"""

from __future__ import annotations

import json
from pathlib import Path

# docs/ root — script lives at docs/_lib/_site.py.
V2 = Path(__file__).resolve().parent.parent
_CONFIG_FILE = V2 / "_site.json"

_DEFAULTS = {
    "site_name": "My Doc-Site",
    "tagline": "Short tagline — replace me",
    "footer": "",  # resolved to "<site_name> docs" below if empty
    "logo_href": "index.html",
}


def _load() -> dict:
    cfg = dict(_DEFAULTS)
    if _CONFIG_FILE.exists():
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg.update({k: v for k, v in data.items() if v is not None})
        except Exception as e:
            print(f"warn: bad _site.json at {_CONFIG_FILE}: {e}")
    if not cfg.get("footer"):
        cfg["footer"] = f"{cfg['site_name']} docs"
    return cfg


SITE = _load()

# Convenience module-level accessors.
SITE_NAME = SITE["site_name"]
TAGLINE = SITE["tagline"]
FOOTER = SITE["footer"]
LOGO_HREF = SITE["logo_href"]
