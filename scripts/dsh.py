#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Mirror the dsh (DeepSeek Harness) docs as markdown.

dsh launched 2026-08-13 as a developer preview with breaking changes
promised -- the `.dsh-plugin` manifest format and `dsh-plugin-prepare`
were deleted 2026-08-09 with no migration path. That churn is why this
mirror tracks it: the docs live in the GitHub repo, not on
api-docs.deepseek.com, so the main fetcher never sees them.

Sources (both fetched from the network, pinned to the default branch):
- github.com/deepseek-ai/deepseek-harness -- README.md plus the English
  docs/ tree (`.zh.md` translations and `.i18n.yaml` sidecars are
  upstream translation infrastructure, not docs; they are skipped).
  Listed via the git trees API, blobs via raw.githubusercontent.com.
- registry.npmjs.org/@deepseek-ai/dsh -- the package publishes no
  readme (as of rc.6), so npm.md renders the packument metadata:
  dist-tags, latest version, version history. A new release shows up
  as a diff on that page.

Content is kept verbatim except two deterministic touches: upstream
YAML frontmatter (VitePress layout metadata) is dropped in favor of
ours, and relative image paths are rewritten to absolute raw URLs so
they render outside the repo. Files deleted upstream are pruned --
with this repo's velocity, deletions are the signal.

    uv run scripts/dsh.py            # write content/en/dsh/
    uv run scripts/dsh.py --check    # exit 1 if the mirror is stale
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from datetime import date
from pathlib import Path

import httpx

REPO = "deepseek-ai/deepseek-harness"
NPM_PACKAGE = "@deepseek-ai/dsh"
API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "en" / "dsh"
UA = "deepseek-docs-mirror/1.0 (+https://github.com/thevibeworks/deepseek-docs)"

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n+", re.S)


def gh_headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def get_json(client: httpx.Client, url: str, headers: dict | None = None) -> dict:
    resp = client.get(url, headers=headers or {"User-Agent": UA})
    resp.raise_for_status()
    return resp.json()


def list_doc_paths(client: httpx.Client, branch: str) -> list[str]:
    """README.md + English docs/**/*.md from the git tree, one request."""
    tree = get_json(
        client, f"{API}/repos/{REPO}/git/trees/{branch}?recursive=1", gh_headers())
    if tree.get("truncated"):
        raise SystemExit("git tree truncated -- the repo outgrew one page")
    paths = [t["path"] for t in tree["tree"] if t["type"] == "blob"]
    return sorted(
        p for p in paths
        if p == "README.md"
        or (p.startswith("docs/") and p.endswith(".md") and not p.endswith(".zh.md")))


def repo_path_to_rel(path: str) -> str:
    """Map an upstream repo path to a path under content/en/dsh/."""
    return "index.md" if path == "README.md" else path


def rewrite_images(body: str, repo_path: str, branch: str) -> str:
    """Relative image paths -> absolute raw URLs (same policy as the main
    fetcher: images point back at the live source)."""
    src_dir = posixpath.dirname(repo_path)

    def sub(m: re.Match) -> str:
        url = m.group(2)
        if url.startswith(("http://", "https://", "data:")):
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(src_dir, url))
        return f"{m.group(1)}{RAW}/{REPO}/{branch}/{resolved}{m.group(3)}"

    return re.sub(r"(!\[[^\]]*\]\()([^)\s]+)(\))", sub, body)


def page_title(body: str, fallback: str) -> str:
    m = re.search(r"^# (.+)$", body, re.M)
    return m.group(1).strip() if m else fallback


def render_page(body: str, title: str, source: str) -> str:
    fm = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"source: {source}",
        f"fetched: {date.today().isoformat()}",
        "---",
        "",
    ]
    return "\n".join(fm) + body.strip() + "\n"


def render_doc(raw: str, repo_path: str, branch: str) -> str:
    body = FRONTMATTER.sub("", raw)
    body = rewrite_images(body, repo_path, branch)
    title = page_title(body, Path(repo_path).stem)
    source = f"https://github.com/{REPO}/blob/{branch}/{repo_path}"
    return render_page(body, title, source)


def render_npm(pkg: dict) -> str:
    latest = pkg["dist-tags"]["latest"]
    v = pkg["versions"][latest]
    times = pkg.get("time", {})
    lines = [
        f"# npm: {NPM_PACKAGE}",
        "",
        v.get("description", ""),
        "",
        "```bash",
        f"npm install -g {NPM_PACKAGE}",
        "```",
        "",
        f"- **latest**: `{latest}`",
    ]
    for tag, ver in sorted(pkg.get("dist-tags", {}).items()):
        if tag != "latest":
            lines.append(f"- **{tag}**: `{ver}`")
    lines += [
        f"- **license**: {v.get('license', 'unknown')}",
        f"- **bin**: {', '.join(f'`{b}`' for b in (v.get('bin') or {}))}",
        f"- **homepage**: {v.get('homepage', '')}",
        "",
        "## Versions",
        "",
    ]
    published = [(ver, times[ver][:10]) for ver in pkg["versions"] if ver in times]
    for ver, day in sorted(published, key=lambda p: (p[1], p[0]), reverse=True):
        lines.append(f"- `{ver}` -- {day}")
    readme = (pkg.get("readme") or v.get("readme") or "").strip()
    if readme:
        lines += ["", "## Readme", "", readme]
    else:
        lines += [
            "",
            "The package publishes no readme; see the",
            f"[repository README](index.md) (github.com/{REPO}).",
        ]
    title = f"npm: {NPM_PACKAGE}"
    source = f"https://www.npmjs.com/package/{NPM_PACKAGE}"
    return render_page("\n".join(lines), title, source)


# ---------------------------------------------------------------- write/check


def strip_fetched(text: str) -> str:
    return re.sub(r"^fetched: .*$", "", text, flags=re.M)


def write_if_changed(out: Path, text: str) -> bool:
    if out.exists() and strip_fetched(out.read_text()) == strip_fetched(text):
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    return True


def write_manifest(results: dict, pruned: list[str]) -> None:
    manifest_path = ROOT / "content" / ".metadata.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    any_changed = any(r.get("changed") for r in results.values()) or bool(pruned)
    files = manifest.setdefault("files", {})
    files.update({k: {kk: vv for kk, vv in v.items() if kk != "changed"}
                  for k, v in results.items()})
    for rel in pruned:
        files.pop(rel, None)
    if any_changed:
        manifest["updated"] = date.today().isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the mirror is stale")
    args = ap.parse_args()

    with httpx.Client(timeout=60, follow_redirects=True) as client:
        branch = get_json(client, f"{API}/repos/{REPO}", gh_headers())["default_branch"]
        doc_paths = list_doc_paths(client, branch)
        print(f"[dsh] {len(doc_paths)} pages from {REPO}@{branch} + npm {NPM_PACKAGE}")

        pages: dict[str, tuple[str, str]] = {}  # rel -> (text, source url)
        for repo_path in doc_paths:
            resp = client.get(f"{RAW}/{REPO}/{branch}/{repo_path}",
                              headers={"User-Agent": UA})
            resp.raise_for_status()
            rel = repo_path_to_rel(repo_path)
            pages[rel] = (render_doc(resp.text, repo_path, branch),
                          f"https://github.com/{REPO}/blob/{branch}/{repo_path}")
        pkg = get_json(client, f"https://registry.npmjs.org/{NPM_PACKAGE}")
        pages["npm.md"] = (render_npm(pkg),
                           f"https://www.npmjs.com/package/{NPM_PACKAGE}")

    expected = {OUT / rel for rel in pages}
    orphans = sorted(p for p in OUT.rglob("*.md") if p not in expected) if OUT.exists() else []

    if args.check:
        stale = [str((OUT / rel).relative_to(ROOT)) for rel, (text, _) in pages.items()
                 if strip_fetched((OUT / rel).read_text() if (OUT / rel).exists() else "")
                 != strip_fetched(text)]
        stale += [str(p.relative_to(ROOT)) + " (deleted upstream)" for p in orphans]
        if stale:
            print("stale:", ", ".join(stale), file=sys.stderr)
            return 1
        print("dsh mirror up to date")
        return 0

    results: dict = {}
    changed_n = 0
    for rel, (text, source) in pages.items():
        out = OUT / rel
        changed = write_if_changed(out, text)
        changed_n += changed
        results[str(out.relative_to(ROOT))] = {
            "url": source, "title": page_title(text, Path(rel).stem),
            "changed": changed}
    pruned = []
    for p in orphans:
        pruned.append(str(p.relative_to(ROOT)))
        p.unlink()
        print(f"  rm  {p.relative_to(ROOT)} (deleted upstream)")
    for d in sorted((d for d in OUT.rglob("*") if d.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    write_manifest(results, pruned)
    print(f"{len(pages)} pages, {changed_n} changed, {len(pruned)} pruned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
