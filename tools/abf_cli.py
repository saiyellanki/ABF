#!/usr/bin/env python3
"""CLI: classify a JSON scoping file and emit a workpaper."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from abf.classify import classify, obligation_applies  # noqa: E402
from abf.library import build_library  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ABF sourced workpaper generator. Reads scoping JSON, writes applicable official IDs."
    )
    parser.add_argument("--answers", required=True, help="Path to scoping answers JSON")
    parser.add_argument("--out", help="Write workpaper JSON to this path (default stdout)")
    args = parser.parse_args()

    answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    lib = build_library()
    result = classify(answers)
    applicable = [o for o in lib["obligations"] if obligation_applies(o, result)]
    workpaper = {
        "disclaimer": lib["disclaimer"],
        "answers": answers,
        "screening": result.to_dict(),
        "applicable_count": len(applicable),
        "applicable": [
            {
                "id": o["id"],
                "framework": o["framework"],
                "citation": o["citation"],
                "source_url": o["source_url"],
                "title": o["title"],
                "official_text": o["official_text"],
                "procedure": o.get("procedure"),
            }
            for o in applicable
        ],
    }
    text = json.dumps(workpaper, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {args.out} applicable={len(applicable)}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
