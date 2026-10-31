---
title: "Fetch"
description: "Fetch a web page and return its title and content as Markdown. See the [Search & Fetch guide](/guides/search) for error handling and billing."
source: https://api-docs.deepseek.com/api/fetch
fetched: 2026-10-31
---

# Fetch

[Open Markdown](https://api-docs.deepseek.com/api/fetch.md "Open Markdown in a new tab")

```
POST /v1/tools/fetch
```

Fetch a web page and return its title and content as Markdown. See the [Search & Fetch guide](../guides/search.md) for error handling and billing.

The response example shows an excerpt of the page content.

## Request

**[application/json]**

**Bodyrequired**

**url** stringrequired

**Minimum characters:** `1`

**Maximum characters:** `8192`

The URL to fetch. Must be at most 8192 characters and an HTTP or HTTPS URL with a host. The URL must not contain a username or password.

## Responses

- 200

OK, returns the fetched page content.

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**title** stringrequired

The title of the page. Empty when the title is unavailable.

**content** stringrequired

The fetched page content as Markdown text.

**[Example]**

```json
{
  "title": "Your First API Call | DeepSeek API Docs",
  "content": "# Your First API Call\n\nThe DeepSeek API uses an API format compatible with OpenAI/Anthropic. By modifying the configuration, you can use the OpenAI/Anthropic SDK or softwares compatible with the OpenAI/Anthropic API to access the DeepSeek API."
}
```

Loading...
