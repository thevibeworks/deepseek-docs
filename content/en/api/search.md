---
title: "Search"
description: "Search the web for a query and return a ranked list of structured results. See the [Search & Fetch guide](/guides/search) for supported query operators, error handling, and billing."
source: https://api-docs.deepseek.com/api/search
fetched: 2026-10-24
---

# Search

```
POST /v1/tools/search
```

Search the web for a query and return a ranked list of structured results. See the [Search & Fetch guide](../guides/search.md) for supported query operators, error handling, and billing.

## Request

**[application/json]**

**Bodyrequired**

**query** stringrequired

**Possible values:** `non-empty` and `<= 128 characters`

The search query. Supports operators such as `site:`, `-site:`, and quoted phrases. Must contain 1 to 128 Unicode characters and cannot be all whitespace.

**count** integer

**Possible values:** `>= 1` and `<= 50`

**Default value:** `10`

The number of results to return, between 1 and 50. Defaults to 10.

**ori\_question** stringnullable

**Possible values:** `non-empty` and `<= 128 characters`

The user's original question that triggered the search, between 1 and 128 characters. Providing it can improve query understanding. `null` is treated as not provided.

**localization** string

An optional IP address used to localize search results. Defaults to an empty string.

**need\_content** boolean

Whether to return page content in `content`. Defaults to `false`; when `false`, `content` is always an empty string.

## Responses

- 200

OK, returns the search results.

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**results**

object[]

required

The search results. Empty when the query matches no results.

- Array [

**rerank\_score** floatrequired

**Possible values:** `<= 3`

A relevance score from 0 to 3 that combines signals such as relevance, authority, and freshness. Scores of 1.5 or above are considered high-quality results.

**title** stringrequired

The title of the search result.

**url** stringrequired

The URL of the search result.

**snippet** stringrequired

A short summary related to the query, typically 100 to 200 characters, intended for display in a UI.

**summary** stringrequired

A long summary related to the query, typically 600 to 800 characters, intended to be read by a model.

**content** stringrequired

The page content. Empty when `need_content` is `false` or when the content is unavailable.

**site\_name** stringnullablerequired

The name of the site, or `null` when unavailable.

**site\_icon** stringnullablerequired

The URL of the site icon, or `null` when unavailable.

**date** date-timenullablerequired

The publication time in UTC, formatted as RFC 3339, or `null` when unknown.

**authority** integerrequired

**Possible values:** `>= -1` and `<= 4`

The authority tier of the page, 0 to 4 (`-1` means unknown). Values of 3 or above indicate highly authoritative sources.

- ]

**[Example (from schema)]**

```json
{
  "results": [
    {
      "rerank_score": 0,
      "title": "string",
      "url": "string",
      "snippet": "string",
      "summary": "string",
      "content": "string",
      "site_name": "string",
      "site_icon": "string",
      "date": "2026-10-19T05:41:50.090Z",
      "authority": 0
    }
  ]
}
```

**[Example]**

```json
{
  "results": [
    {
      "rerank_score": 2.4,
      "title": "DeepSeek V4 model released",
      "url": "https://example.com/deepseek-v4",
      "snippet": "DeepSeek V4 is now available, with tool calling and long-context support.",
      "summary": "DeepSeek has released the V4 model. The release adds improved tool calling and long-context support for agent workflows.",
      "content": "DeepSeek V4 is now generally available...",
      "site_name": "Example News",
      "site_icon": "https://example.com/favicon.ico",
      "date": "2026-06-01T00:00:00+00:00",
      "authority": 3
    }
  ]
}
```

Loading...
