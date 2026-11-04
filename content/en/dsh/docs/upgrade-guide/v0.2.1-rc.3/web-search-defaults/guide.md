---
title: "Web search defaults"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.3/web-search-defaults/guide.md
fetched: 2026-11-03
---
# Web search defaults

English | [中文](guide.zh.md)

## Change

In `dsh-tool-web`, the `searchMaxQueries` default rises from 4 to 10 and the `searchMaxResults` default rises from 8 to 10. The `web_search` schema now advertises `1–10 search queries`, so a call with 5–10 queries runs instead of failing validation, and each call can return up to 10 sources. A call can therefore start more provider searches and add more source text to the context. With the shipped Messages search provider, each query is one auxiliary model request. `dsh-web-deepseek-api` adds `searchRequestsPerSecond`, default 5: its Search provider sends at most that many requests in any one-second window, so the second five queries of a 10-query call start one second after the first instead of exceeding the account's 5 QPS limit. Values that a deployment already sets are kept.

## Migration

1. To keep the previous limits, set `searchMaxQueries: 4` and `searchMaxResults: 8` in the `tool-web` entry's `config` in `cordis.patch.yml`.
2. If several processes share one DeepSeek account through the Search API, lower `searchRequestsPerSecond` in the `web-deepseek-api` entry so that their combined rate stays at or below 5.
3. Confirm the result by running a task that sends 10 queries in one `web_search` call: it returns results instead of `Error: queries must contain at most 4 queries`. See the [tool-web configuration](../../../../packages/web/tool-web/README.md).
