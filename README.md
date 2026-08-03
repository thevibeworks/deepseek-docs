# DeepSeek API Docs Mirror

> Unofficial markdown mirror of [api-docs.deepseek.com](https://api-docs.deepseek.com/).
> 126 pages (en + zh-cn), built for LLM agents: plain markdown, stable paths,
> `llms.txt` index, `llms-full.txt` single-file dump.

Clone this repo and point your coding agent at it. Every DeepSeek API doc --
quick start, API reference, guides, samples, agent integrations, news --
searchable, version-controlled, and offline.

## Install

```bash
git clone https://github.com/thevibeworks/deepseek-docs
cd deepseek-docs
```

Then ask your agent anything:

```bash
claude "how do I enable thinking mode on deepseek-v4-pro?"
claude "what's the Anthropic-format base URL and which params map to what?"
claude "show me the FIM completion request schema"
```

## Content

```
content/
  en/                       English docs (63 pages)
    index.md                Your First API Call
    quick_start/            pricing, rate limits, error codes, token usage
    quick_start/agent_integrations/   Claude Code, Codex, OpenCode, ... (18 tools)
    api/                    API reference: chat completions, responses,
                            FIM, models, balance (from the OpenAPI-rendered pages)
    guides/                 thinking mode, tool calls, JSON mode, KV cache,
                            Anthropic API, Responses API, FIM, prefix completion
    api_samples/            curl / python / nodejs request samples
    news/                   release notes (V3, R1, V3.1, V4, ...)
    faq.md  updates.md  prompt-library.md
  zh-cn/                    Chinese mirror, identical paths
llms.txt                    curated index of every English page
llms-full.txt               all English pages concatenated (~320 KB)
sources.json                machine-readable source registry
```

Every file carries frontmatter with its canonical `source:` URL and fetch
date. Internal links are rewritten to relative `.md` paths so they resolve
inside the repo; images point back at the live site.

## Fetching

```bash
# Requires: uv (https://docs.astral.sh/uv/)
uv run scripts/fetcher.py                # fetch everything (en + zh-cn)
uv run scripts/fetcher.py --locale en    # one locale
uv run scripts/fetcher.py --incremental  # skip existing files
uv run scripts/fetcher.py --index-only   # rebuild llms.txt / llms-full.txt
uv run scripts/fetcher.py --tree         # show sources + counts
```

The site is Docusaurus v3 with no llms.txt and no markdown variants, so the
fetcher discovers pages via `sitemap.xml` (per locale) and converts the
server-rendered HTML article body to markdown locally. The prompt library is
the one client-rendered page; its data is fetched from the site's static
`prompts.json` instead.

## Automation

[`fetch-deepseek-docs.yml`](.github/workflows/fetch-deepseek-docs.yml)
runs every 6 hours: fetch, then hand the diff to Claude Code running on
the **DeepSeek API itself** (`deepseek-v4-flash` via the
Anthropic-compatible endpoint, `anthropic_api_key` = a `DEEPSEEK_API_KEY`
repo secret). The agent only classifies the change and writes decision
files; a deterministic bash step publishes -- minor changes commit
straight to main, high-signal changes (new models, pricing, API schema)
open a PR for human review. DeepSeek docs, kept fresh by DeepSeek.

## Disclaimer

Unofficial mirror for educational and development purposes. Documentation
content belongs to DeepSeek; for official docs visit
[api-docs.deepseek.com](https://api-docs.deepseek.com/). Code in this repo
is MIT-licensed.
