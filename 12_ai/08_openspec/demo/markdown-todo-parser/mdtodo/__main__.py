"""CLI: python -m mdtodo <file> [--json]"""
from __future__ import annotations

import argparse
import json
import sys

from . import parse_file


def main() -> int:
    ap = argparse.ArgumentParser(prog="mdtodo", description="Extract TODOs from markdown")
    ap.add_argument("file", help="Markdown file path")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    try:
        items = parse_file(args.file)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([i.to_dict() for i in items], ensure_ascii=False, indent=2))
    else:
        if not items:
            print("(no TODOs)")
            return 0
        for it in items:
            mark = "x" if it.status == "done" else " "
            sec = f"[{it.section}] " if it.section else ""
            print(f"L{it.line:>4} [{mark}] {sec}{it.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
