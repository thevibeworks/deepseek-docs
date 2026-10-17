---
title: "Fetch"
description: "Fetch a web page and return its title and content as Markdown. See the [Search & Fetch guide](/guides/search) for error handling and billing."
source: https://api-docs.deepseek.com/api/fetch
fetched: 2026-10-17
---

# Fetch

```
POST /v1/tools/fetch
```

Fetch a web page and return its title and content as Markdown. See the [Search & Fetch guide](../guides/search.md) for error handling and billing.

## Request

**[application/json]**

**Bodyrequired**

**url** stringrequired

**Possible values:** `non-empty` and `<= 8192 characters`

The URL to fetch. Must be at most 8192 characters and an HTTP or HTTPS URL with a host. The URL must not contain a username or password.

## Responses

- 200

OK, returns the fetched page content.

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**title** stringrequired

The title of the page. Empty when the title is unavailable.

**content** stringrequired

The fetched page content as Markdown text.

**[Example (from schema)]**

```json
{
  "title": "string",
  "content": "string"
}
```

**[Example]**

```json
{
  "title": "Example article",
  "content": "# Example article\n\nArticle content."
}
```

Loading...
