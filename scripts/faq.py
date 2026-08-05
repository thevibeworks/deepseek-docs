#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Mirror DeepSeek's FAQ as markdown.

The FAQ at https://static.deepseek.com/faq/ is not part of the Docusaurus
site the main fetcher walks, and it has no sitemap, no llms.txt and no
server-rendered HTML — index.html is a 562-byte shell. The content is a
`JSON.parse('...')` blob inside the main JS chunk, holding both locales as
mdast (the markdown AST remark produces), so it round-trips back to
markdown exactly rather than being scraped out of rendered DOM.

That makes it brittle in one specific way: the chunk filename is
content-hashed, so it changes on every deploy. We read index.html to find
the current one instead of pinning it.

    uv run scripts/faq.py            # write content/<locale>/faq/
    uv run scripts/faq.py --check    # exit 1 if the mirror is stale

Outputs one file per category, because that is how the FAQ is navigated
(#/category/4 is the API section) and how anyone answering a question
would want to read it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import httpx

INDEX = "https://static.deepseek.com/faq/index.html?lang=en"
BASE = "https://static.deepseek.com/faq/"
ROOT = Path(__file__).resolve().parent.parent
LOCALES = {"en": "en", "zh": "zh-cn"}  # their key -> our directory


def find_bundle(client: httpx.Client) -> str:
    """The main JS chunk, whose name carries a content hash."""
    html = client.get(INDEX).text
    for src in re.findall(r'src="([^"]+)"', html):
        if "/main." in src and src.endswith(".js"):
            return src if src.startswith("http") else BASE + src.lstrip("/")
    raise SystemExit("no main.*.js in the FAQ shell — the bundle layout changed")


def extract(js: str) -> dict:
    """Pull the JSON.parse('...') payload out of the bundle.

    It is a single-quoted JS string literal, so the JSON inside it keeps
    its own escapes: `\\"` in the source is a backslash-escape at the JS
    level producing `\\"` for JSON. Decoding therefore has to happen in
    two passes, JS first, and neither can be a naive replace.
    """
    start = js.find("JSON.parse('{\"zh\":{\"categories\"")
    if start < 0:
        raise SystemExit("FAQ payload not found — the bundle layout changed")

    i = start + len("JSON.parse('")
    raw = []
    while i < len(js):
        ch = js[i]
        if ch == "\\":
            raw.append(js[i : i + 2])
            i += 2
            continue
        if ch == "'":
            break
        raw.append(ch)
        i += 1

    simple = {
        "n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f",
        "v": "\v", "0": "\0", "\\": "\\", "'": "'", '"': '"', "/": "/",
    }
    out, lit, i = [], "".join(raw), 0
    while i < len(lit):
        c = lit[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        nxt = lit[i + 1]
        if nxt == "u":
            out.append(chr(int(lit[i + 2 : i + 6], 16)))
            i += 6
        elif nxt == "x":
            out.append(chr(int(lit[i + 2 : i + 4], 16)))
            i += 4
        else:
            out.append(simple.get(nxt, nxt))
            i += 2
    return json.loads("".join(out))


def md(node: dict) -> str:
    """mdast -> markdown, for the node types this content actually uses."""
    t = node.get("type")
    if t == "text":
        return node.get("value", "")
    if t == "inlineCode":
        return f"`{node.get('value', '')}`"
    if t == "code":
        return f"```{node.get('lang') or ''}\n{node.get('value', '')}\n```\n\n"
    if t == "html":
        return node.get("value", "")
    if t == "image":
        return f"![{node.get('alt') or ''}]({node.get('url', '')})"
    if t == "thematicBreak":
        return "---\n\n"

    inner = "".join(md(k) for k in node.get("children", []))
    if t == "paragraph":
        return inner + "\n\n"
    if t == "heading":
        return "#" * (node.get("depth", 3) + 2) + " " + inner + "\n\n"
    if t == "list":
        return inner + "\n"
    if t == "listItem":
        body = inner.strip().replace("\n\n", "\n  ")
        return f"- {body}\n"
    if t == "link":
        return f"[{inner}]({node.get('url', '')})"
    if t == "strong":
        return f"**{inner}**"
    if t == "emphasis":
        return f"*{inner}*"
    if t == "blockquote":
        return "> " + inner.strip().replace("\n", "\n> ") + "\n\n"
    if t == "break":
        return "\n"
    if t == "table":
        return inner + "\n"
    return inner


def render(category: dict, locale_dir: str, fetched: str) -> str:
    slug = category["id"]
    url = f"https://static.deepseek.com/faq/index.html?lang={'en' if locale_dir == 'en' else 'zh'}#/category/{slug}"
    # Upstream's own `description` is template junk — every category in
    # both locales reads "{title}相关问题", untranslated in en and
    # doubled in zh ("API相关相关问题"). It carries nothing the title does
    # not, so we write our own rather than mirror a filler string.
    count = len(category["questions"])
    lines = [
        "---",
        f'title: "FAQ: {category["title"]}"',
        f'description: "DeepSeek FAQ, {category["title"]} — {count} questions and answers."',
        f"source: {url}",
        f"fetched: {fetched}",
        "---",
        "",
        f"# FAQ: {category['title']}",
        "",
    ]
    for q in category["questions"]:
        lines.append(f"## {q['title']}")
        lines.append("")
        lines.append("".join(md(n) for n in q["answer"]).strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if the mirror is stale")
    args = ap.parse_args()

    with httpx.Client(timeout=60, follow_redirects=True) as client:
        data = extract(client.get(find_bundle(client)).text)

    fetched = date.today().isoformat()
    stale, written = [], []
    for key, locale_dir in LOCALES.items():
        if key not in data:
            print(f"warning: locale {key} missing from the FAQ payload", file=sys.stderr)
            continue
        out_dir = ROOT / "content" / locale_dir / "faq"
        for category in data[key]["categories"]:
            path = out_dir / f"category-{category['id']}.md"
            text = render(category, locale_dir, fetched)
            if args.check:
                # The fetched: line moves every run; compare the rest.
                old = path.read_text() if path.exists() else ""
                if strip_fetched(old) != strip_fetched(text):
                    stale.append(str(path.relative_to(ROOT)))
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            written.append(f"{path.relative_to(ROOT)} ({len(category['questions'])}q)")

    if args.check:
        if stale:
            print("stale:", ", ".join(stale), file=sys.stderr)
            return 1
        print("faq mirror up to date")
        return 0
    for line in written:
        print("  ==", line)
    print(f"{len(written)} category files")
    return 0


def strip_fetched(text: str) -> str:
    return re.sub(r"^fetched: .*$", "", text, flags=re.M)


if __name__ == "__main__":
    sys.exit(main())
