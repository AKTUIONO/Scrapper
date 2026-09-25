"""Daily frontier-tech scout.

  python -m scrapper run       # collect -> ideas (if ANTHROPIC_API_KEY) -> render
  python -m scrapper collect   # only write data/<date>/digest.json
  python -m scrapper render    # re-render using data/<date>/ideas.json if present
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from . import collect, ideas, render

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "data" / "ideas_history.json"


def _load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(prog="scrapper")
    ap.add_argument("command", choices=["run", "collect", "render"])
    ap.add_argument("--date", default=time.strftime("%Y-%m-%d", time.gmtime()))
    ap.add_argument("--ideas", type=int, default=3)
    ap.add_argument("--force", action="store_true", help="regenerate ideas even if saved")
    args = ap.parse_args()

    day = ROOT / "data" / args.date
    digest_path, ideas_path = day / "digest.json", day / "ideas.json"

    if args.command in ("run", "collect"):
        digest = collect.collect()
        _write(digest_path, digest)
        print(f"Collected {len(digest['podcasts'])} podcast episodes, "
              f"{len(digest['news'])} news items, {len(digest['errors'])} feed errors")
        if args.command == "collect":
            return
    digest = _load(digest_path, None)
    if digest is None:
        sys.exit(f"No digest for {args.date}; run collect first")

    history = _load(HISTORY, [])
    briefing = None if args.force else _load(ideas_path, None)
    if briefing is None and args.command == "run":
        if os.environ.get("ANTHROPIC_API_KEY"):
            print("ANTHROPIC_API_KEY found; generating ideas with Claude")
            briefing = ideas.generate(digest, history, args.ideas)
            _write(ideas_path, briefing)
            print(f"Generated {len(briefing['ideas'])} ideas")
        else:
            print("ANTHROPIC_API_KEY not set; skipping idea generation")
    if briefing:
        new = [i["title"] for i in briefing["ideas"] if i["title"] not in history]
        _write(HISTORY, history + new)

    out = ROOT / "briefings" / f"{args.date}.md"
    out.write_text(render.render(args.date, digest, briefing))
    (ROOT / "briefings" / "LATEST.md").write_text(out.read_text())
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
