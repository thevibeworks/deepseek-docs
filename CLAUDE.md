# CLAUDE.md

Markdown mirror of https://api-docs.deepseek.com/ (DeepSeek API docs),
126 pages across en and zh-cn locales. Answer DeepSeek API questions from
`content/en/` and cite the `source:` URL in each file's frontmatter.

## Finding things

Start from `llms.txt` (curated index of every English page). Key entry
points:

- `content/en/index.md` - first API call, base URLs, auth
- `content/en/quick_start/pricing.md` - models (deepseek-v4-flash /
  deepseek-v4-pro), context length, feature matrix, prices
- `content/en/api/create-chat-completion.md` - full chat/completions schema
- `content/en/api/create-response.md` - OpenAI Responses API format
- `content/en/guides/anthropic_api.md` - Anthropic-format endpoint
- `content/en/guides/thinking_mode.md` - reasoning toggle + effort mapping
- `content/en/guides/tool_calls.md` - function calling
- `content/en/quick_start/agent_integrations/` - per-tool setup (Claude
  Code, Codex, OpenCode, ...)
- `content/en/news/` - model release notes, newest = highest date prefix

`content/zh-cn/` mirrors the same paths in Chinese. Prefer `en` unless the
user asks in Chinese; the prompt library content is Chinese-only.

## Freshness

Docs are a snapshot; `fetched:` frontmatter dates each file. DeepSeek ships
model changes frequently -- for time-sensitive answers (prices, model
versions), say when the mirror was fetched and offer to refetch:

```bash
uv run scripts/fetcher.py            # refetch everything (~30s)
uv run scripts/fetcher.py --index-only   # rebuild llms.txt / llms-full.txt
```

## Maintaining the fetcher

`scripts/fetcher.py` is a single-file uv script (aiohttp + bs4 +
markdownify). Source registry lives in `sources.json`. The site is
Docusaurus v3, fully SSR except `/prompt-library` (client-rendered from
`/zh-cn/data/prompts.json`, special-cased in the fetcher). Unknown paths
return HTTP 200 with the SPA shell -- never trust status codes alone when
probing for new endpoints.

After changing conversion logic, re-run a full fetch and spot-check:
code fences keep indentation and raw underscores, internal links resolve
as relative `.md` paths, no `CODEBLOCKTOKEN` leftovers.
