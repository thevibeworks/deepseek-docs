# DeepSeek API Docs Mirror

> Unofficial markdown mirror of [api-docs.deepseek.com](https://api-docs.deepseek.com/).
> 134 pages (en + zh-cn), built for LLM agents: plain markdown, stable paths,
> `llms.txt` index, `llms-full.txt` single-file dump. Includes the FAQ, which
> is not part of the docs site and is not readable as text anywhere else,
> and the [dsh (DeepSeek Harness)](content/en/dsh/) docs, which live on
> GitHub/npm rather than the docs site.

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

## The FAQ

`content/*/faq/` does not come from the docs site. DeepSeek's FAQ lives at
`static.deepseek.com/faq/`, whose `index.html` is a 562-byte shell — the
content is a `JSON.parse('...')` blob inside a content-hashed JavaScript
chunk, held as [mdast](https://github.com/syntax-tree/mdast) rather than
HTML. `scripts/faq.py` finds the current chunk, decodes the blob and
renders the AST back to markdown, so the result round-trips rather than
being scraped out of rendered DOM.

It is worth the trouble: 44 questions per locale, 15 of them about the API,
covering things api-docs never mentions — invoices, refunds, what to do
about a leaked key, how to request a higher rate limit.

```bash
uv run scripts/faq.py            # refresh content/<locale>/faq/
uv run scripts/faq.py --check    # exit 1 if stale
```

## dsh (DeepSeek Harness)

`content/en/dsh/` mirrors [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
(launched 2026-08-13) -- the repo README, its English `docs/` tree, and a
metadata page for the [`@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh)
npm package. These docs live on GitHub/npm, not on api-docs, so the main
fetcher never sees them.

dsh is a developer preview that ships breaking changes without migration
paths (the `.dsh-plugin` manifest format and `dsh-plugin-prepare` were
deleted 2026-08-09, cold). That is exactly why it is mirrored here: the
sync diff is the changelog upstream does not write. Pages deleted upstream
are pruned, so deletions show up in the diff too.

Community companions to this mirror: [howto-dsh](https://github.com/dshworks/howto-dsh)
(verified traps, dated against specific dsh versions),
[awesome-dsh-plugins](https://github.com/dshworks/awesome-dsh-plugins)
(spam-filtered plugin registry), and the [dshworks](https://dshworks.github.io)
org index.

```bash
uv run scripts/dsh.py            # refresh content/en/dsh/
uv run scripts/dsh.py --check    # exit 1 if stale
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
    faq/                    the FAQ, one file per category, extracted from
                            static.deepseek.com (see above)
    dsh/                    dsh (DeepSeek Harness) docs from GitHub + npm
                            (see above); index.md = repo README, docs/ =
                            the repo's English docs tree, npm.md = package
    faq.md  updates.md  prompt-library.md
  zh-cn/                    Chinese mirror, identical paths (api-docs only)
llms.txt                    curated index of every English page
llms-full.txt               all English api-docs pages concatenated (~330 KB;
                            the dsh section is indexed but not concatenated)
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
runs every 6 hours: fetch (dsh from GitHub/npm, then the api-docs site),
then hand the diff to Claude Code running on
the **DeepSeek API itself** (`deepseek-v4-flash` via the
Anthropic-compatible endpoint, `anthropic_api_key` = a `DEEPSEEK_API_KEY`
repo secret). The agent only classifies the change and writes decision
files; a deterministic bash step publishes -- minor changes commit
straight to main, high-signal changes (new models, pricing, API schema,
dsh breaking changes) open a PR for human review. A deterministic
pricing tripwire overrides the agent: any pricing.md diff touching
time-of-day tier language (时段 / off-peak / peak / discount /
multiplier / 分时) is forced high-signal, because the peak-hour plan
was dropped 2026-08-08 with a repricing pending and downstream
consumers need to hear about its return the same day. DeepSeek docs,
kept fresh by DeepSeek.

## Disclaimer

Unofficial mirror for educational and development purposes. Documentation
content belongs to DeepSeek; for official docs visit
[api-docs.deepseek.com](https://api-docs.deepseek.com/). Code in this repo
is MIT-licensed.
