#!/usr/bin/env python3
"""Write data/library.json for the static web app."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from abf.library import build_library  # noqa: E402


def main() -> None:
    out = ROOT / "data" / "library.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    lib = build_library()
    out.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {out} obligations={len(lib['obligations'])} "
        f"procedures={lib['procedure_count']} sources={len(lib['sources'])}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
