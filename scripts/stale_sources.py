#!/usr/bin/env python3
"""Report pages this mirror still holds but no longer successfully fetches.

A mirror can commit every six hours, keep a green pipeline and a fresh
`main`, and still be quietly wrong: the aggregate looks alive because most
pages update, while one page has been serving a fallback shell for weeks
and the copy in the repo is a fossil nobody flagged. Freshness of the whole
cannot see staleness of a part.

Upstream flaps, so a single failing run means nothing. `error_since` in
content/.metadata.json records when a page's error first appeared and
survives only while it keeps failing; anything holding one past the
threshold has stopped being a blip and become a fact about the mirror.

The threshold is measured, not guessed. Replaying every manifest commit
from 2026-08-02 to 09-02 for the three flappiest pages (news250120 en and
zh-cn, news1226 en) gives error spells of 0, 1, 3, 4 and 5 days -- 27
spells, longest 5. Seven days would have fired zero times across that
month, so it stays silent on upstream having a bad week and speaks only
when a page has actually stopped coming back.

Exit 0 and print nothing when every source is healthy.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / "content" / ".metadata.json"
DEFAULT_DAYS = 7


def stale(manifest: dict, days: int, today: date) -> list[tuple[int, str, str]]:
    out = []
    for path, meta in sorted(manifest.get("files", {}).items()):
        if not isinstance(meta, dict) or "error" not in meta:
            continue
        since = meta.get("error_since")
        if not since:
            continue
        try:
            age = (today - date.fromisoformat(since)).days
        except ValueError:
            continue
        if age >= days:
            out.append((age, path, meta["error"]))
    return sorted(out, reverse=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS,
                    help=f"flag errors at least this old (default {DEFAULT_DAYS})")
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--github-output", action="store_true",
                    help="also emit stale=<count> for GITHUB_OUTPUT")
    args = ap.parse_args()

    if not args.manifest.exists():
        print(f"no manifest at {args.manifest}", file=sys.stderr)
        return 0
    manifest = json.loads(args.manifest.read_text())
    rows = stale(manifest, args.days, date.today())

    for age, path, err in rows:
        print(f"{age:>4}d  {path}\n        {err}")
    if args.github_output:
        print(f"stale={len(rows)}")
    if rows:
        print(f"\n{len(rows)} source(s) unfetched for {args.days}+ days",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
