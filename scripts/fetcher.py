#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "aiohttp>=3.9",
#     "beautifulsoup4>=4.12",
#     "markdownify>=0.13",
# ]
# ///
"""Mirror https://api-docs.deepseek.com/ as an LLM-friendly markdown vault.

The site is Docusaurus v3 (fully server-rendered, no llms.txt, no .md
variants), so we discover pages via sitemap.xml per locale, extract the
article body from the HTML, and convert it to markdown locally.

Usage:
    uv run scripts/fetcher.py                      # fetch all locales
    uv run scripts/fetcher.py --locale en          # one locale
    uv run scripts/fetcher.py --incremental        # skip existing files
    uv run scripts/fetcher.py --tree               # show sources + counts
    uv run scripts/fetcher.py --index-only         # regenerate llms.txt from content/

Outputs:
    content/<locale>/<path>.md    one file per page, with frontmatter
    content/.metadata.json        per-file fetch manifest
    llms.txt                      curated index (root, en)
    llms-full.txt                 all en docs concatenated
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SOURCES = json.loads((ROOT / "sources.json").read_text())

SITE = SOURCES["site"]["base_url"].rstrip("/")
LOCALES = SOURCES["site"]["locales"]  # {"en": "", "zh-cn": "/zh-cn"}
CONCURRENCY = 8
UA = "deepseek-docs-mirror/1.0 (+https://github.com/thevibeworks/deepseek-docs)"

# ---------------------------------------------------------------- discovery


async def fetch_text(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()


def sitemap_urls(xml: str) -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def url_to_relpath(url: str, locale: str) -> str:
    """Map a page URL to a path under content/<locale>/."""
    prefix = LOCALES[locale]
    path = urlparse(url).path
    if prefix and path.startswith(prefix):
        path = path[len(prefix):]
    path = path.strip("/")
    if not path:
        path = "index"
    return f"{path}.md"


# ---------------------------------------------------------------- conversion


class FallbackPageError(ValueError):
    """Server returned the SPA shell instead of the requested page."""

LANG_ALIASES = {"jsx": "jsx", "tsx": "tsx", "bash": "bash", "shell": "bash"}


def code_block_text(code_el) -> str:
    """Docusaurus renders each code line as span.token-line; plain get_text()
    would drop the newlines between lines."""
    lines = code_el.select("span.token-line")
    if lines:
        return "\n".join(ln.get_text() for ln in lines)
    return code_el.get_text()


def detect_language(pre) -> str:
    node = pre
    for _ in range(4):
        if node is None:
            break
        classes = " ".join(node.get("class") or [])
        m = re.search(r"language-([\w-]+)", classes)
        if m:
            return m.group(1)
        node = node.parent
    return ""


def rewrite_links(article, locale: str, self_rel: str, page_paths: set[str]) -> None:
    """Make links work inside the vault: internal doc links become relative
    .md links; site assets become absolute URLs."""
    import posixpath
    prefix = LOCALES[locale]
    self_dir = posixpath.dirname(self_rel)

    def to_md_rel(path: str) -> str | None:
        if prefix and path.startswith(prefix):
            path = path[len(prefix):] or "/"
        clean = path.strip("/") or "index"
        if clean not in page_paths:
            return None
        return posixpath.relpath(f"{clean}.md", self_dir or ".")

    for a in article.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if href.startswith("/"):
            path, _, frag = href.partition("#")
            rel = to_md_rel(path)
            if rel:
                a["href"] = rel + (f"#{frag}" if frag else "")
            else:
                a["href"] = SITE + href
    for img in article.find_all("img", src=True):
        if img["src"].startswith("/"):
            img["src"] = SITE + img["src"]


def preprocess(article: BeautifulSoup) -> list[str]:
    """Mutate the article DOM into something markdownify converts cleanly.
    Returns the extracted code blocks; they are swapped in for placeholder
    tokens after conversion so markdownify cannot escape or reflow them."""
    # Anchor permalinks render as stray "[​](#...)" links -- drop them.
    for a in article.select("a.hash-link"):
        a.decompose()
    # Copy buttons, edit links, screen-reader-only helpers.
    for sel in ("button", ".theme-code-block-copied", ".sr-only",
                "[class*=codeButton]", "[class*=buttonGroup]"):
        for el in article.select(sel):
            el.decompose()
    # Code blocks -> placeholder tokens, swapped back in after conversion
    # (running the fence through markdownify would escape underscores and
    # collapse indentation).
    code_blocks: list[str] = []
    for pre in article.find_all("pre"):
        code = pre.find("code")
        text = code_block_text(code) if code else pre.get_text()
        lang = detect_language(pre)
        code_blocks.append(f"```{lang}\n{text}\n```")
        token = f"\n\nCODEBLOCKTOKEN{len(code_blocks) - 1}ENDTOKEN\n\n"
        pre.replace_with(NavigableString(token))
    # Tabs: label each panel with its tab title so nothing reads ambiguous.
    for container in article.select(".tabs-container"):
        tabs = [t.get_text(strip=True) for t in container.select('[role="tab"]')]
        panels = container.select('[role="tabpanel"]')
        for title, panel in zip(tabs, panels):
            heading = BeautifulSoup(f"<p><strong>[{title}]</strong></p>", "html.parser")
            panel.insert(0, heading)
            if panel.has_attr("hidden"):
                del panel["hidden"]
        tablist = container.select_one('[role="tablist"]')
        if tablist:
            tablist.decompose()
    # <details> panels (API schemas): keep content, promote summary to bold.
    for details in article.find_all("details"):
        summary = details.find("summary")
        if summary:
            summary.replace_with(BeautifulSoup(
                f"<p><strong>{summary.get_text(strip=True)}</strong></p>",
                "html.parser"))
    # Tables nested inside bold/emphasis wrappers produce broken "**|" rows.
    for tag in article.find_all(["strong", "b", "em"]):
        if tag.find("table"):
            tag.unwrap()
    return code_blocks


def html_to_markdown(html: str, url: str, locale: str, self_rel: str,
                     page_paths: set[str]) -> tuple[str, dict]:
    soup = BeautifulSoup(html, "html.parser")
    title_el = soup.select_one("title")
    title = title_el.get_text().split("|")[0].strip() if title_el else ""
    desc_el = soup.select_one('meta[name="description"]')
    description = desc_el["content"].strip() if desc_el and desc_el.get("content") else ""

    # The server answers unknown/hiccuped paths with HTTP 200 and the SPA
    # shell carrying the homepage article; without this guard those save as
    # silent homepage duplicates (bit us on two news pages, 2026-08-02).
    canon = soup.select_one('link[rel="canonical"]')
    if canon and canon.get("href"):
        canon_path = urlparse(canon["href"]).path.rstrip("/") or "/"
        req_path = urlparse(url).path.rstrip("/") or "/"
        if canon_path != req_path:
            raise FallbackPageError(
                f"served fallback shell for {url} (canonical: {canon['href']})")

    article = (soup.select_one("article div.theme-doc-markdown")
               or soup.select_one("article")
               or soup.select_one("main"))
    if article is None:
        raise ValueError(f"no article container in {url}")
    rewrite_links(article, locale, self_rel, page_paths)
    code_blocks = preprocess(article)
    body = markdownify(str(article), heading_style="ATX", bullets="-")
    body = re.sub(
        r"CODEBLOCKTOKEN(\d+)ENDTOKEN",
        lambda m: code_blocks[int(m.group(1))],
        body)
    # Collapse the whitespace debris conversion leaves behind.
    body = re.sub(r"​", "", body)
    body = re.sub(r"[ \t]+$", "", body, flags=re.M)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    meta = {"title": title, "description": description}
    return body, meta


def render_page(body: str, meta: dict, url: str) -> str:
    fm = ["---", f"title: {json.dumps(meta['title'], ensure_ascii=False)}"]
    if meta["description"]:
        fm.append(
            f"description: {json.dumps(meta['description'], ensure_ascii=False)}")
    fm += [f"source: {url}", f"fetched: {date.today().isoformat()}", "---", ""]
    return "\n".join(fm) + "\n" + body


# ---------------------------------------------------------------- fetch loop


def write_if_changed(out: Path, text: str) -> bool:
    """Skip the write when only the fetched: date differs -- keeps re-fetch
    diffs (and the sync automation reading them) free of timestamp churn."""
    strip = lambda s: re.sub(r"^fetched: .*$", "", s, flags=re.M)  # noqa: E731
    if out.exists() and strip(out.read_text()) == strip(text):
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    return True

# The prompt-library page is client-rendered from a static JSON (the only
# such page on the site); everything else is SSR HTML.
PROMPTS_JSON = "/zh-cn/data/prompts.json"


def render_prompt_library(prompts: list[dict], url: str) -> str:
    lines = [
        "# Prompt Library (提示库)",
        "",
        f"{len(prompts)} ready-to-use prompt examples from the DeepSeek prompt",
        "library. The site publishes these in Chinese only (both locales).",
        "In each example, the final assistant message is the sample output.",
        "",
    ]
    for p in prompts:
        lines += [f"## {p['title']}", "", p.get("description", ""), ""]
        msgs = p.get("messages", [])
        for m in msgs[:-1]:
            lines += [f"**Prompt ({m['role']}):**", "",
                      "````text", m["content"], "````", ""]
        if msgs:
            lines += ["**Sample output:**", "",
                      "````text", msgs[-1]["content"], "````", ""]
    meta = {"title": "Prompt Library (提示库)",
            "description": "DeepSeek prompt library: ready-to-use prompt examples with sample outputs."}
    return render_page("\n".join(lines).strip() + "\n", meta, url)


async def fetch_prompt_library(session, url: str, out: Path, results: dict):
    try:
        data = json.loads(await fetch_text(session, SITE + PROMPTS_JSON))
        changed = write_if_changed(out, render_prompt_library(data, url))
        results[str(out.relative_to(ROOT))] = {
            "url": url, "data": SITE + PROMPTS_JSON,
            "title": "Prompt Library (提示库)", "changed": changed}
        print(f"  {'ok ' if changed else '== '} {out.relative_to(ROOT)} (from {PROMPTS_JSON})")
    except Exception as e:  # noqa: BLE001
        results[str(out.relative_to(ROOT))] = {"url": url, "error": str(e)}
        print(f"  ERR {url}: {e}", file=sys.stderr)


async def fetch_page(session, sem, url: str, out: Path, results: dict,
                     locale: str, page_paths: set[str]):
    rel = url_to_relpath(url, locale)
    if rel == "prompt-library.md":
        async with sem:
            await fetch_prompt_library(session, url, out, results)
        return
    async with sem:
        try:
            for attempt in range(3):
                html = await fetch_text(session, url)
                try:
                    body, meta = html_to_markdown(
                        html, url, locale, rel, page_paths)
                    break
                except FallbackPageError:
                    if attempt == 2:
                        raise
                    await asyncio.sleep(2.0 * (attempt + 1))
            changed = write_if_changed(out, render_page(body, meta, url))
            results[str(out.relative_to(ROOT))] = {
                "url": url, "title": meta["title"], "changed": changed}
            print(f"  {'ok ' if changed else '== '} {out.relative_to(ROOT)}")
        except Exception as e:  # noqa: BLE001 - report and continue
            results[str(out.relative_to(ROOT))] = {"url": url, "error": str(e)}
            print(f"  ERR {url}: {e}", file=sys.stderr)


async def run_fetch(locales: list[str], incremental: bool) -> dict:
    sem = asyncio.Semaphore(CONCURRENCY)
    results: dict = {}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(
            timeout=timeout, headers={"User-Agent": UA}) as session:
        for locale in locales:
            prefix = LOCALES[locale]
            sitemap = f"{SITE}{prefix}/sitemap.xml"
            urls = sitemap_urls(await fetch_text(session, sitemap))
            print(f"[{locale}] {len(urls)} pages from {sitemap}")
            page_paths = {url_to_relpath(u, locale)[:-3] for u in urls}
            tasks = []
            for url in urls:
                rel = url_to_relpath(url, locale)
                out = CONTENT / locale / rel
                if incremental and out.exists():
                    continue
                tasks.append(fetch_page(session, sem, url, out, results,
                                        locale, page_paths))
            await asyncio.gather(*tasks)
    return results


# ---------------------------------------------------------------- indexing

SECTION_ORDER = [
    ("Getting Started", ["index.md", "quick_start/pricing.md",
                         "quick_start/rate_limit.md", "quick_start/error_codes.md",
                         "quick_start/token_usage.md"]),
    ("API Reference", ["api/"]),
    ("Guides", ["guides/"]),
    ("API Samples", ["api_samples/"]),
    ("Agent Integrations", ["quick_start/agent_integrations/"]),
    ("News & Updates", ["news/", "updates.md"]),
    ("dsh (DeepSeek Harness)", ["dsh/"]),
    ("Other", ["faq.md", "prompt-library.md"]),
]


def read_meta(path: Path) -> dict:
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = {"title": path.stem, "description": ""}
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("title: "):
                meta["title"] = json.loads(line[7:])
            elif line.startswith("description: "):
                meta["description"] = json.loads(line[13:])
    return meta


def collect_en_files() -> list[Path]:
    return sorted((CONTENT / "en").rglob("*.md"))


def section_for(rel: str) -> str:
    # exact-file entries win over directory prefixes
    for name, patterns in SECTION_ORDER:
        if rel in patterns:
            return name
    for name, patterns in SECTION_ORDER:
        for p in patterns:
            if p.endswith("/") and rel.startswith(p):
                return name
    return "Other"


def build_llms_txt() -> None:
    files = collect_en_files()
    grouped: dict[str, list[tuple[str, dict]]] = {}
    for f in files:
        rel = str(f.relative_to(CONTENT / "en"))
        grouped.setdefault(section_for(rel), []).append((rel, read_meta(f)))

    lines = [
        "# DeepSeek API Docs",
        "",
        "> Unofficial markdown mirror of https://api-docs.deepseek.com/ -- the",
        "> DeepSeek API documentation (OpenAI/Anthropic-compatible chat, reasoning,",
        "> tool calls, pricing, agent integrations). English pages listed below;",
        "> a Chinese mirror lives in content/zh-cn/ with identical paths.",
        "> The dsh section mirrors github.com/deepseek-ai/deepseek-harness and",
        "> npm (@deepseek-ai/dsh), not api-docs -- see scripts/dsh.py.",
        "",
        "Each file carries frontmatter with its canonical `source:` URL.",
        "",
    ]
    for name, _ in SECTION_ORDER:
        entries = grouped.get(name)
        if not entries:
            continue
        lines.append(f"## {name}")
        lines.append("")
        for rel, meta in entries:
            desc = f": {meta['description']}" if meta["description"] else ""
            if len(desc) > 160:
                desc = desc[:157] + "..."
            lines.append(f"- [{meta['title']}](content/en/{rel}){desc}")
        lines.append("")
    (ROOT / "llms.txt").write_text("\n".join(lines))
    print(f"llms.txt: {sum(len(v) for v in grouped.values())} entries")


def build_llms_full() -> None:
    # The dsh section (github/npm source, ~1.5 MB on its own) is indexed in
    # llms.txt but not concatenated here; this stays the api-docs dump.
    parts = ["<!-- llms-full.txt: every English page of the DeepSeek API docs "
             "mirror, concatenated. See llms.txt for the index. -->\n"]
    for f in collect_en_files():
        rel = str(f.relative_to(ROOT))
        if rel.startswith("content/en/dsh/"):
            continue
        parts.append(f"\n\n<!-- ===== {rel} ===== -->\n\n{f.read_text()}")
    (ROOT / "llms-full.txt").write_text("".join(parts))
    size = (ROOT / "llms-full.txt").stat().st_size
    print(f"llms-full.txt: {size // 1024} KB")


def write_manifest(results: dict) -> None:
    manifest_path = CONTENT / ".metadata.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    any_changed = any(r.get("changed") for r in results.values())
    manifest.setdefault("files", {}).update(
        {k: {kk: vv for kk, vv in v.items() if kk != "changed"}
         for k, v in results.items()})
    if any_changed or "updated" not in manifest:
        manifest["updated"] = date.today().isoformat()
    manifest["site"] = SITE
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------- cli


def show_tree() -> None:
    print(f"site: {SITE}")
    for locale, prefix in LOCALES.items():
        d = CONTENT / locale
        count = len(list(d.rglob("*.md"))) if d.exists() else 0
        print(f"  {locale:8} {SITE}{prefix}/sitemap.xml  ({count} files mirrored)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--locale", choices=[*LOCALES, "all"], default="all")
    ap.add_argument("--incremental", action="store_true",
                    help="skip pages whose output file already exists")
    ap.add_argument("--tree", action="store_true", help="show sources and exit")
    ap.add_argument("--index-only", action="store_true",
                    help="rebuild llms.txt / llms-full.txt from content/")
    args = ap.parse_args()

    if args.tree:
        show_tree()
        return
    if not args.index_only:
        locales = list(LOCALES) if args.locale == "all" else [args.locale]
        results = asyncio.run(run_fetch(locales, args.incremental))
        write_manifest(results)
        errors = [r for r in results.values() if "error" in r]
        if errors:
            print(f"{len(errors)} pages failed", file=sys.stderr)
    build_llms_txt()
    build_llms_full()


if __name__ == "__main__":
    main()
