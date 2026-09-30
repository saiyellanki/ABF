"""Print ABF walkthrough procedures (official IDs only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from abf.library import build_library  # noqa: E402
from abf.procedures import PROCEDURES  # noqa: E402


def render_markdown(control_ids: list[str] | None = None) -> str:
    lib = build_library()
    by_id = {o["id"]: o for o in lib["obligations"]}
    lines = [
        "# ABF technical walkthrough packet",
        "",
        lib["disclaimer"],
        "",
        "Procedures below are ABF workpapers mapped to official identifiers.",
        "",
    ]
    selected = PROCEDURES
    if control_ids:
        wanted = {c.upper() for c in control_ids}
        selected = [
            p
            for p in PROCEDURES
            if p["id"].upper() in wanted
            or p["primary"].upper() in wanted
            or p["primary"].replace("NIST-", "").replace("EU-", "").upper() in wanted
        ]
    for proc in selected:
        src = by_id.get(proc["primary"], {})
        lines.extend(
            [
                f"## {proc['primary']}: {proc['title']}",
                f"**Official citation:** {src.get('citation', proc['primary'])}",
                f"**Source:** {src.get('source_url', '')}",
                f"**Target roles:** {', '.join(proc['target_roles'])}",
                "",
                "### Architectural inquiry",
                f"> {proc['inquiry']}",
                "",
                "### What to observe",
                proc["observe"],
                "",
                "### Evidence",
                *[f"- [ ] {item}" for item in proc["evidence"]],
                "",
                "### Test procedure",
                proc["test"],
                "",
                f"_{proc.get('authored_by', 'ABF workpaper procedure')}_",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="ABF walkthrough generator (sourced IDs)")
    parser.add_argument("--control", action="append", help="Official ID or procedure ID (repeatable)")
    parser.add_argument("--export-json", action="store_true")
    args = parser.parse_args()
    if args.export_json:
        print(json.dumps(PROCEDURES, indent=2))
        return 0
    print(render_markdown(args.control))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
