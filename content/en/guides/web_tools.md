---
title: "Web Tools"
description: "DeepSeek provides two server tools that give the model the web capabilities of DeepSeek Chat. The model decides whether to go online, and searching and fetching run on the service. Your client does not execute any tool."
source: https://api-docs.deepseek.com/guides/web_tools
fetched: 2026-11-14
---

# Web Tools

DeepSeek provides two server tools that give the model the web capabilities of DeepSeek Chat. The model decides whether to go online, and searching and fetching run on the service. Your client does not execute any tool.

To call search and fetch directly from your own code, use the [Search & Fetch](search.md) APIs instead.

| Capability | How to enable it | What it does |
| --- | --- | --- |
| [Web search](#web-search) | Declare `deepseek_web_search`, thinking disabled | The model searches the web when the question calls for it, and answers with citations |
| [Deep thinking search](#search-while-thinking) | Declare `deepseek_web_search`, thinking enabled | Over several reasoning steps the model searches, opens pages and finds text in pages on its own, checking facts as it reasons |
| [URL reading](#read-links) | Declare `deepseek_read_url` | The model finds the links in the user message, fetches the pages, and answers with their content in context |

Available in the Messages API, the Responses API and the Chat Completions API. Most of this page describes the format in the Messages API; the formats in the other two are described in [Responses API](#responses-api) and [Chat Completions API](#chat-completions-api) below.

Use the `deepseek-flash` model.

---

## Declare the Tools

Declare the tools you want in `tools`. This request turns on both:

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "thinking": {"type": "enabled"},
    "tools": [
      {"type": "deepseek_web_search", "name": "deepseek_web_search"},
      {"type": "deepseek_read_url", "name": "deepseek_read_url"}
    ],
    "messages": [{"role": "user", "content": "What is new in DeepSeek V4.1?"}],
    "stream": true
  }'
```

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "reasoning": {"effort": "high"},
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "input": "What is new in DeepSeek V4.1?",
    "stream": true
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "thinking": {"type": "enabled"},
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "messages": [{"role": "user", "content": "What is new in DeepSeek V4.1?"}],
    "stream": true
  }'
```

To read links without searching, declare only `deepseek_read_url`.

`tool_choice` cannot name `deepseek_web_search` or `deepseek_read_url`; otherwise the request returns `400`. The model decides whether to search or read links. With `tool_choice` set to `none`, all the tools are turned off, including URL reading.

---

## Web Search

With thinking disabled, the model decides whether to search, and answers with citations, like web search in DeepSeek Chat.

- One search can contain several queries, all listed in `input.queries`.
- Each search produces a `server_tool_use` block with `input.action` and `kind` set to `search`, followed by a `web_search_tool_result` block. The answer cites the results with [`citations`](#citations).
- To turn search off, do not declare `deepseek_web_search`; declare only `deepseek_read_url` to keep URL reading.

A request with thinking disabled that asks "What is the population of Iceland?" returns the following. The search returned three results, of which one is shown, and `encrypted_content` is shortened.

```json
{
  "id": "18f3b95b-bf3c-4ffb-8c90-ad50d7cfb211",
  "type": "message",
  "role": "assistant",
  "model": "deepseek-flash",
  "content": [
    {
      "type": "server_tool_use",
      "id": "srvtoolu_s_00_72b1a35619ec4611884415c48d35ba34",
      "name": "deepseek_web_search",
      "input": {
        "action": "search",
        "queries": ["Iceland population 2024", "Iceland population 2025"]
      },
      "caller": {"type": "direct"},
      "kind": "search"
    },
    {
      "type": "web_search_tool_result",
      "tool_use_id": "srvtoolu_s_00_72b1a35619ec4611884415c48d35ba34",
      "content": [
        {
          "type": "web_search_result",
          "title": "2024年冰岛人口总数、净移民人口数、劳动人口数及人口性别、年龄及城乡结构分析",
          "url": "https://www.huaon.com/channel/globaldata/1112834.html",
          "encrypted_content": "6sesWdNHoulpcfritukyowXu...",
          "page_age": "2025-10-15T16:00:00+00:00",
          "snippet": "华经产业研究院数据显示：冰岛是高收入国家之一，2024年冰岛人口总数为40.46万人，比上年增长了1.13万人...",
          "site_name": "华经情报网",
          "site_icon": "https://cdn.deepseek.com/site-icons/huaon.com"
        }
      ],
      "kind": "search"
    },
    {
      "type": "text",
      "text": "Iceland's population is approximately **394,000** (as of early 2026), based on data from Statistics Iceland",
      "citations": [
        {
          "type": "web_search_result_location",
          "url": "https://wallstreetcn.com/livenews/3197120",
          "title": "快讯：根据冰岛统计局（Statistics Iceland）的一份预测，冰岛人口将在四分之一个世纪内达到50万，高于2026年初的39.4 万。",
          "encrypted_index": "",
          "cited_text": "Iceland's population is approximately **394,000** (as of early 2026), based on data from Statistics Iceland"
        }
      ]
    },
    {
      "type": "text",
      "text": ".\n\nDifferent sources may have slight variations due to different statistical time points or estimation methods. For reference, data from 2024 shows a population of approximately **404,600** at that time",
      "citations": [
        {
          "type": "web_search_result_location",
          "url": "https://www.huaon.com/channel/globaldata/1112834.html",
          "title": "2024年冰岛人口总数、净移民人口数、劳动人口数及人口性别、年龄及城乡结构分析",
          "encrypted_index": "",
          "cited_text": ".\n\nDifferent sources may have slight variations due to different statistical time points or estimation methods. For reference, data from 2024 shows a population of approximately **404,600** at that time"
        }
      ]
    },
    {"type": "text", "text": "."}
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 1905,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 72,
    "service_tier": "standard",
    "server_tool_use": {"web_search_requests": 1, "web_fetch_requests": 0, "tool_search": 2, "tool_fetch": 0, "tool_image_search": 0}
  }
}
```

### Image Search

Image search is part of the `deepseek_web_search` tool: when the user message contains images, the model can search by image, also during [deep thinking search](#search-while-thinking).

An image search has the same call and result structure as a web search, with three differences:

- `kind` is `image_search`, or `deep_image_search` during deep thinking search.
- There are no queries: `queries` is an empty array.
- Each result has an extra `image_url` field, the address of the image on its original site, for display only. It may be absent, and it is not guaranteed to be reachable.

For billing, see [Usage and Billing](#billing).

---

## Deep Thinking Search

With thinking enabled, `deepseek_web_search` works as deep thinking search: over several thinking steps the model searches, opens pages, and finds text in pages, like deep thinking search in DeepSeek Chat.

- The model makes up to about 20 tool calls before it answers.

| `content[].input.action` | Step |
| --- | --- |
| `search` | Search the web |
| `open_page` | Open a page |
| `find_in_page` | Find text in an opened page |

- Every step is a `server_tool_use` block with `kind` set to `deep_search`, followed by its result. When the model calls several tools at once, the calls come first and the results follow.
- Opening pages here is part of `deepseek_web_search`: the model opens pages it found while searching. It is different from reading the links that the user sent, which is done by `deepseek_read_url`.
- Opened pages return only the URL, title and publication time: `data` is an empty string and there is no `signature`.

An [image search](#image-search) during deep thinking search has `kind` set to `deep_image_search`.

A request that asks "Which is taller, the Eiffel Tower or the Tokyo Tower? Check their official sites." returns these blocks, in this order:

```text
thinking
server_tool_use         search        4 queries
web_search_tool_result
thinking
server_tool_use         open_page     https://www.toureiffel.paris/en/the-monument/key-figures
server_tool_use         open_page     https://en.tokyotower.co.jp/company/
web_fetch_tool_result
web_fetch_tool_result
thinking
server_tool_use         open_page     https://en.tokyotower.co.jp/
server_tool_use         find_in_page  pattern "330"
server_tool_use         find_in_page  pattern "meter"
server_tool_use         find_in_page  pattern "333"
web_fetch_tool_result   (4 results)
thinking
server_tool_use         search        3 queries
web_search_tool_result
thinking
server_tool_use         open_page     (2 calls)
web_fetch_tool_result   (2 results)
thinking
text                    4 blocks, 3 of them with citations
```

One call and its result from that response. The result of `find_in_page` has the same form, with `title` set to `null`.

```json
[
  {
    "type": "server_tool_use",
    "id": "srvtoolu_ds_02_7e545ef1967b433eb8c0bfdfca520c89",
    "name": "deepseek_web_search",
    "input": {"action": "open_page", "url": "https://en.tokyotower.co.jp/company/"},
    "caller": {"type": "direct"},
    "kind": "deep_search"
  },
  {
    "type": "web_fetch_tool_result",
    "tool_use_id": "srvtoolu_ds_02_7e545ef1967b433eb8c0bfdfca520c89",
    "content": {
      "type": "web_fetch_result",
      "url": "https://en.tokyotower.co.jp/company/",
      "content": {
        "type": "document",
        "source": {"type": "text", "media_type": "text/plain", "data": ""},
        "title": "Tokyo Tower is a Tokyo landmark, standing 333 meters tall."
      },
      "published_at": null
    },
    "kind": "deep_search"
  }
]
```

---

## URL Reading

When the last user message contains URLs, `deepseek_read_url` lets the model read those pages and answer based on them, like URL reading in DeepSeek Chat.

- Only the last user message is checked for URLs. Repeated URLs count once. At most the first 10 different URLs in the message are considered, and the model decides which of them to read.
- With thinking enabled and `deepseek_web_search` declared, the round uses [deep thinking search](#search-while-thinking) and does not read links separately. Links are read only otherwise: with thinking disabled, or with only `deepseek_read_url` declared. A round is the span from one user message to the final answer of the model, and corresponds to one request.
- Each page read produces a `server_tool_use` block with `input.action` set to `read_link` and the `url`, and a `web_fetch_tool_result` block with `kind` set to `read_link`. When several links are read at once, all calls come first and the results follow.
- The result has the URL, title and publication date of the page. The page text is not returned in the block; it is carried encrypted in `signature`. The `url`, `title`, `data` and `published_at` fields are for display only; changing them before passing the block back has no effect.
- When several links are read in one round, each page gets less room, so long pages are truncated.
- With [model content safety](safety.md) enabled, read-link results are sent only after they pass the review. A page that does not pass returns a `url_not_allowed` error.

---

## Response Blocks

Every call produces a `server_tool_use` block and a result block. When streaming, the content of both kinds of block arrives all at once in `content_block_start`, not in increments.

Match calls to results by `tool_use_id`. When several pages are read at once, or when model content safety is enabled, a result does not always follow its call. Every call gets a result: if a call does not finish, its result is an `unavailable` error.

### server\_tool\_use

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_s_00_3f2a9c...",
  "name": "deepseek_web_search",
  "input": {"action": "search", "queries": ["DeepSeek V4.1"]},
  "caller": {"type": "direct"},
  "kind": "search"
}
```

| `content[].input.action` | `content[].name` | Other `input` fields |
| --- | --- | --- |
| `search` | `deepseek_web_search` | `queries`: the search queries of this call |
| `open_page` | `deepseek_web_search` | `url` |
| `find_in_page` | `deepseek_web_search` | `url` and `pattern` |
| `read_link` | `deepseek_read_url` | `url` |

- `name` is the declared tool that enabled the capability. It is not one of the names in the Anthropic SDK types, but the SDKs do not check it at runtime. `input.action` and `kind` are DeepSeek extensions. `kind` tells which capability the call belongs to: `search` (web search), `deep_search` (deep thinking search), `read_link` (URL reading), and `image_search` or `deep_image_search` ([image search](#image-search)).

### web\_search\_tool\_result

```json
{
  "type": "web_search_tool_result",
  "tool_use_id": "srvtoolu_s_00_3f2a9c...",
  "content": [
    {
      "type": "web_search_result",
      "title": "...",
      "url": "https://example.com/news",
      "encrypted_content": "...",
      "page_age": "2026-01-02T03:04:05+00:00",
      "snippet": "...",
      "site_name": "Example News",
      "site_icon": "https://cdn.deepseek.com/site-icons/example.com"
    }
  ],
  "kind": "search"
}
```

- `content` can be an empty array. A failed search returns `[{"type": "web_search_tool_result_error", "error_code": "unavailable"}]`.
- `snippet`, `site_name` and `site_icon` are DeepSeek extensions for display. `site_name` and `site_icon` can be `null`. They are ignored when passed back.
- Image search results also have `image_url`; see [Image Search](#image-search).
- `page_age` is an RFC 3339 UTC timestamp, or `null`.

### web\_fetch\_tool\_result

```json
{
  "type": "web_fetch_tool_result",
  "tool_use_id": "srvtoolu_rl_01_9c1d...",
  "content": {
    "type": "web_fetch_result",
    "url": "https://example.com/a",
    "content": {
      "type": "document",
      "source": {"type": "text", "media_type": "text/plain", "data": ""},
      "title": "Page title"
    },
    "published_at": "2026-01-01"
  },
  "kind": "read_link",
  "signature": "q3J0b1RmZ1c4cE1x..."
}
```

- The page text is not returned: `data` is always an empty string. For `read_link`, the page is carried encrypted in `signature`; pass the block back unchanged so that the page is restored into the context. See [Multi-turn Conversations](#multi-turn).
- `published_at`: for `read_link` it is the date found on the page, in no fixed format; for pages opened during deep thinking search it is an RFC 3339 timestamp. Both can be `null`.
- A failed fetch has `content` set to `{"type": "web_fetch_tool_result_error", "error_code": "..."}` and no `signature`:

| `error_code` | Meaning |
| --- | --- |
| `url_not_accessible` | The link could not be read |
| `url_not_allowed` | Reading the link is not allowed, or the page did not pass the model content safety review |
| `unavailable` | The service is unavailable, a page could not be opened during deep thinking search, or the call did not finish |

---

## Citations

When the answer cites sources, its `text` blocks carry `citations`:

```json
{
  "type": "text",
  "text": "It is cloudy in Shanghai today.",
  "citations": [
    {
      "type": "web_search_result_location",
      "url": "https://example.com/weather",
      "title": "...",
      "encrypted_index": "",
      "cited_text": "It is cloudy in Shanghai today."
    }
  ]
}
```

- In a stream, each citation arrives as a `citations_delta` event on the current `text` block.
- Once a `text` block has a citation, the following text starts a new `text` block, so the citations of a block belong to its own text. A URL appears at most once per block.
- `type` is always `web_search_result_location`, also for pages opened during deep thinking search. `cited_text` is the answer text of the block up to the citation, not text quoted from the source. `encrypted_index` is always an empty string, and `title` can be `null`.
- Citations are ignored when passed back.

---

## Streaming

A request with thinking enabled that searches once produces events in this order:

```text
message_start
content_block_start (thinking) → thinking_delta … → signature_delta → content_block_stop
content_block_start (server_tool_use) → content_block_stop
content_block_start (web_search_tool_result) → content_block_stop
content_block_start (thinking) → thinking_delta … → signature_delta → content_block_stop
content_block_start (text) → text_delta … → citations_delta … → content_block_stop
content_block_start (text) → text_delta … → content_block_stop
message_delta
message_stop
```

- With thinking enabled, a `thinking` block opens right after `message_start`. It can be empty when the model searches first.
- The `usage` in `message_start` covers only the first inference step. Read the final usage from `message_delta`.
- With [`title`](conversation_title.md) enabled, `message_delta` also carries the conversation title.
- While nothing new is produced, the stream sends `: keep-alive` comments, and a non-streaming request receives newline characters before the JSON body. See [Rate Limit](../quick_start/rate_limit.md).

### Stop Reasons

| `stop_reason` | Meaning |
| --- | --- |
| `end_turn` | The answer is complete |
| `max_tokens` | The output reached the maximum length, and the answer is cut off; or the context ran out after searching or reading links |
| `refusal` | Content review refused the response; see [Model Content Safety](safety.md#handling-refusals) |

---

## Multi-turn Conversations

Send the full history on every request, and pass each previous reply back unchanged, including the `kind` and `signature` fields.

- Search results, opened pages and the thinking of earlier rounds are not added to the context of later rounds; only the answer text is.
- History that contains web tool blocks can also be sent in requests that do not declare these tools.
- A page read from a link is restored from its `signature` and added to the end of the user message of that round, so the model can refer to it in later rounds. Without a valid `signature`, the page is not added and the request still succeeds.

For example, the first round read a link, and the second round passes that reply back. The ids and the `signature` are shortened here.

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search", "name": "deepseek_web_search"},
      {"type": "deepseek_read_url", "name": "deepseek_read_url"}
    ],
    "messages": [
      {"role": "user", "content": "Summarize https://example.com/ in one sentence."},
      {
        "role": "assistant",
        "content": [
          {
            "type": "server_tool_use",
            "id": "srvtoolu_rl_00_0efde247...",
            "name": "deepseek_read_url",
            "input": {"action": "read_link", "url": "https://example.com"},
            "caller": {"type": "direct"},
            "kind": "read_link"
          },
          {
            "type": "web_fetch_tool_result",
            "tool_use_id": "srvtoolu_rl_00_0efde247...",
            "content": {
              "type": "web_fetch_result",
              "url": "https://example.com",
              "content": {
                "type": "document",
                "source": {"type": "text", "media_type": "text/plain", "data": ""},
                "title": "Example Domain"
              },
              "published_at": null
            },
            "kind": "read_link",
            "signature": "tQU8k+8Ko7MY5XDAvJd0..."
          },
          {"type": "text", "text": "The example.com domain is reserved for use in documentation examples."}
        ]
      },
      {"role": "user", "content": "Quote the first sentence of that page."}
    ]
  }'
```

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "input": [
      {"role": "user", "content": "Summarize https://example.com/ in one sentence."},
      {
        "type": "web_search_call",
        "id": "srvtoolu_rl_00_0efde247...",
        "status": "completed",
        "kind": "read_link",
        "action": {"type": "open_page", "url": "https://example.com"},
        "page": {"url": "https://example.com", "title": "Example Domain", "published_at": null},
        "signature": "tQU8k+8Ko7MY5XDAvJd0..."
      },
      {
        "type": "message",
        "role": "assistant",
        "content": [{"type": "output_text", "text": "The example.com domain is reserved for use in documentation examples."}]
      },
      {"role": "user", "content": "Quote the first sentence of that page."}
    ]
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "messages": [
      {"role": "user", "content": "Summarize https://example.com/ in one sentence."},
      {
        "role": "assistant",
        "content": "The example.com domain is reserved for use in documentation examples.",
        "server_tool_calls": [
          {
            "index": 0,
            "reasoning_content": "",
            "calls": [
              {
                "index": 0,
                "id": "srvtoolu_rl_00_0efde247...",
                "type": "deepseek_read_url",
                "kind": "read_link",
                "action": {"type": "read_link", "url": "https://example.com"},
                "status": "completed",
                "page": {"url": "https://example.com", "title": "Example Domain", "published_at": null},
                "signature": "tQU8k+8Ko7MY5XDAvJd0..."
              }
            ]
          }
        ]
      },
      {"role": "user", "content": "Quote the first sentence of that page."}
    ]
  }'
```

---

## Continue Generation

To continue an interrupted reply, end the messages with the partial `assistant` message. The response contains only the new part.

- A reply that used `deepseek_web_search` or `deepseek_read_url` cannot be continued and returns `400`. Resend the previous request instead.
- In the Chat Completions API, set `prefix: true` on the last `assistant` message and use the beta endpoint. The Responses API does not support continuing a reply.

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "messages": [
      {"role": "user", "content": "Write a short poem about autumn."},
      {"role": "assistant", "content": "The autumn wind rises,"}
    ]
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/beta/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "messages": [
      {"role": "user", "content": "Write a short poem about autumn."},
      {"role": "assistant", "content": "The autumn wind rises,", "prefix": true}
    ]
  }'
```

---

## Usage and Billing

The `usage` in the final `message_delta`, or in a non-streaming response, is the billed usage of the whole request, summed over its inference steps:

| Field | Meaning |
| --- | --- |
| `input_tokens` | Input tokens not served from the context cache |
| `cache_read_input_tokens` | Input tokens served from the context cache |
| `output_tokens` | Output tokens |
| `output_tokens_details.thinking_tokens` | The thinking tokens among them, returned when thinking is enabled |
| `cache_creation_input_tokens` | Always `0` |
| `server_tool_use.web_search_requests`, `web_fetch_requests` | The numbers of search result blocks and fetch result blocks in the response, including errors. They are for display and are not billed counts |
| `server_tool_use.tool_search`, `tool_fetch`, `tool_image_search` | The billed numbers of searches (excluding image searches), fetches and image searches |

Tool calls are billed separately, at the web search, image search and web fetch prices in [Models & Pricing](../quick_start/pricing.md#web-tools-pricing), the same prices as the Search and Fetch APIs:

- Web search: a search call that returns results is billed for each of its queries, so a call with three queries counts as three. A call that fails or returns no results is not billed.
- Image search: each image counts as 1 search, and each region the model selects in an image counts as 1 more. A search that fails or finds no results is not billed.
- Web fetch, URL reading: per page fetched successfully, including pages whose result is then replaced by a `url_not_allowed` or `unavailable` error under model content safety. Links that cannot be fetched are not billed.
- Web fetch, deep thinking search: an opened page is billed only when it is fetched from the web. Opening the same page again, moving through a page, and opening a page whose content came with the search results are free.
- Finding text in a page is free.

---

## Errors

An input blocked by content review returns `400 Content Exists Risk`. A request whose context exceeds the model limit returns `400`.

Common error messages:

| Cause | `error.message` |
| --- | --- |
| A tool is declared twice | `` tools: `deepseek_web_search` can only be declared once `` |
| Another server tool is declared | `` tools: other tools cannot be used together with `deepseek_web_search`, `deepseek_read_url`, `safety_check` or `title` yet `` |
| A tool has `allowed_domains`, `blocked_domains` or `user_location` | `` tools: `allowed_domains` is not supported by `deepseek_web_search` `` |
| `tool_choice` names a declared web tool | `` tool_choice: `deepseek_web_search` cannot be forced `` |
| `safety_check` has no valid `level` | `` safety_check: `level` must be `low` or `high` `` |
| The reply to continue used a web tool | `` messages: the last `assistant` message used `deepseek_web_search` or `deepseek_read_url` and cannot be continued; resend the previous request `` |

### Generation Failures

If an error occurs after the answer has started to generate, such as an inference timeout or interruption, the HTTP status is already `200`. The response ends with an error and carries `usage`. Inference, searches and page reads that ran before the failure are billed as usual.

| Protocol | Streaming | Non-streaming |
| --- | --- | --- |
| Messages | Ends with an `error` event, with no `message_delta` or `message_stop` after it | The body is `{"type": "error", "error": {...}, "usage": {...}}` |
| Responses | Ends with a `response.failed` event | `status` is `failed` and `error.code` is `server_error` |
| Chat Completions | The last chunk carries `error` with empty `choices`, and no `[DONE]` follows | The body is `{"error": {...}, "usage": {...}}` |

```text
event: error
data: {"type":"error","error":{"type":"api_error","message":"The model failed to generate a complete response. Please retry."},"usage":{...}}
```

A non-streaming response has status `200`, so SDKs do not raise an exception. Check the body for `error` (check `status` in the Responses API).

---

## Responses API

The same tools work in the [Responses API](responses_api.md). Declare them in `tools`, and set `safety_check` and `title` at the top level, as in the Messages API. `tool_choice: "required"` is treated as `auto`.

```json
{
  "model": "deepseek-flash",
  "input": "What is new in DeepSeek V4.1?",
  "tools": [
    {"type": "deepseek_web_search"},
    {"type": "deepseek_read_url"}
  ],
  "safety_check": {"level": "high"},
  "stream": true
}
```

### Request

- `web_search` cannot be declared together with these tools, and `custom`, `namespace` and `tool_search` tools are not supported; both return `400`. Other tool types that are not recognized are ignored.
- `text.format` other than `text`, `top_logprobs`, `previous_response_id` and `conversation` return `400`. The response reports `store: false`.
- `item_reference` and unknown input item types return `400`.
- Some parameters are ignored; see [Ignored Parameters](build_a_chatbot.md#ignored-parameters).
- `instructions` and `system` or `developer` messages are merged into one system prompt.
- An `input` that ends with an assistant `message` or `reasoning` item returns `400` (continuing a reply is not supported in the Responses API).

### Output

Each tool call is a `web_search_call` item with the DeepSeek extension `kind`:

```json
{
  "type": "web_search_call",
  "id": "srvtoolu_s_00_3f2a9c...",
  "status": "completed",
  "kind": "search",
  "action": {
    "type": "search",
    "queries": ["DeepSeek V4.1"],
    "sources": [
      {
        "type": "url",
        "url": "https://example.com/news",
        "title": "...",
        "snippet": "...",
        "site_name": "Example News",
        "site_icon": "https://cdn.deepseek.com/site-icons/example.com",
        "published_at": "2026-01-02T03:04:05+00:00"
      }
    ]
  }
}
```

| `output[].kind` | `output[].action.type` | Other fields |
| --- | --- | --- |
| `search`, `deep_search`, `image_search` and `deep_image_search` | `search` | `action.queries`, and `action.sources` with the display fields `title`, `snippet`, `site_name`, `site_icon` and `published_at` |
| `deep_search` | `open_page` or `find_in_page` (with `pattern`) | `page`: `{url, title, published_at}` for an opened page |
| `read_link` | `open_page` | `page`, and `signature` when the page was read |

- A failed call has `status: "failed"` and `error: {"code": "..."}`, with the codes listed under [web\_fetch\_tool\_result](#web_fetch_tool_result).
- Thinking is a `reasoning` item with `reasoning_text` content and an empty `summary`, without `encrypted_content`.
- The answer is a `message` item. Its `output_text` carries the citations as `url_citation` annotations; `start_index` and `end_index` count Unicode code points, and `title` is an empty string when unknown.

| `status` | Meaning |
| --- | --- |
| `completed` | The answer is complete |
| `incomplete`, `incomplete_details.reason: "max_output_tokens"` | The output reached the maximum length, and the answer is cut off |
| `incomplete`, `incomplete_details.reason: "content_filter"` | Content review refused the response. `output` keeps only the executed `web_search_call` items; see [Model Content Safety](safety.md#handling-refusals) |

### Streaming

- A call produces `response.output_item.added`, with the complete `action`, then `response.web_search_call.in_progress`, `response.web_search_call.searching`, `response.web_search_call.completed`, and `response.output_item.done` with `sources`, `page`, `signature` or `error`.
- When several calls run at once, all of them are added first and then completed one by one. Match the events by `output_index`.
- Each citation is sent as a `response.output_text.annotation.added` event.
- With the OpenAI Python SDK, `get_final_response()` raises an error when the response ends with `content_filter`; read the final response from the `response.incomplete` event instead.

### Usage

- In `usage.server_tool_use`, `tool_search` is the number of billed searches (excluding image searches), `tool_fetch` the number of billed fetches, and `tool_image_search` the number of billed image searches. The field is omitted when all three are `0`.

### Multi-turn Conversations

Pass the previous `output` items back in `input` unchanged, including `kind` and `signature`; the rules are the same as in [Multi-turn Conversations](#multi-turn). `web_search_call` items produced by the `web_search` tool are treated as searches.

---

## Chat Completions API

The same tools work in the Chat Completions API, through extension fields of the request and the response.

Declare the tools in `tools`, and set `safety_check` and `title` at the top level, as in the other protocols. `tool_choice: "required"` is treated as `auto`.

### Request

- `web_search_options` returns `400` in a request that declares these tools; declare the tools in `tools` instead.
- `response_format` other than `text`, `logprobs` and `top_logprobs` return `400`.
- Some parameters are ignored; see [Ignored Parameters](build_a_chatbot.md#ignored-parameters).
- [`latest_reminder`](latest_reminder.md) messages are accepted.
- A reply is continued only with `prefix: true` on the last `assistant` message, on the beta endpoint; see [Continue Generation](#continue-generation).

### Output

The tool calls are in the extension field `message.server_tool_calls`. Each entry is one step: the thinking of the step and the calls it made.

```json
{
  "role": "assistant",
  "reasoning_content": "I have enough to answer ...",
  "content": "The post is about ... The author previously worked at ...",
  "annotations": [
    {"type": "url_citation", "url_citation": {"url": "https://example.com/post", "title": "...", "start_index": 0, "end_index": 21}}
  ],
  "server_tool_calls": [
    {
      "index": 0,
      "reasoning_content": "",
      "calls": [
        {
          "index": 0,
          "id": "srvtoolu_rl_00_3f2a...",
          "type": "deepseek_read_url",
          "kind": "read_link",
          "action": {"type": "read_link", "url": "https://example.com/post"},
          "status": "completed",
          "page": {"url": "https://example.com/post", "title": "...", "published_at": "2026-01-02"},
          "signature": "q3J0b1RmZ1c4cE1x..."
        }
      ]
    },
    {
      "index": 1,
      "reasoning_content": "I have read the post. Next, the author's background ...",
      "calls": [
        {
          "index": 0,
          "id": "srvtoolu_s_01_9c41...",
          "type": "deepseek_web_search",
          "kind": "search",
          "action": {"type": "search", "queries": ["..."]},
          "status": "completed",
          "sources": [
            {"type": "url", "url": "https://example.com/news", "title": "...", "snippet": "...", "site_name": "Example News", "site_icon": "...", "published_at": "2026-01-02T03:04:05+00:00"}
          ]
        }
      ]
    }
  ]
}
```

| Level | Field | Meaning |
| --- | --- | --- |
| Step | `index` | The number of the step, from 0 |
| Step | `reasoning_content` | The thinking of this step. With thinking enabled it is always a string, empty when the step has no thinking; with thinking disabled the field is omitted |
| Step | `calls` | The calls made in this step, in order |
| Call | `index`, `id` | The number of the call within the step, and its `id` in the same form as in the other protocols |
| Call | `type` | The declared tool that enabled the capability: `deepseek_web_search` or `deepseek_read_url` |
| Call | `kind` | `search`, `deep_search`, `read_link`, `image_search` or `deep_image_search` |
| Call | `action` | The arguments: `{type: "search", queries}`, `{type: "open_page", url}`, `{type: "find_in_page", url, pattern}` or `{type: "read_link", url}` |
| Call | `status` | `completed` or `failed`. A call that has no result when the response ends is `failed` |
| Call | `sources` | The results of a search, with the same display fields as in the Responses API |
| Call | `page` | `{url, title, published_at}` of an opened page or a link that was read, for display |
| Call | `signature` | The encrypted page, only on a link that was read successfully |
| Call | `error` | `{code}` of a failed call, with the codes listed under [web\_fetch\_tool\_result](#web_fetch_tool_result) |

- `message.reasoning_content` holds only the thinking of the last step; the thinking of earlier steps is in their entries.
- `content` has no citation markers. The citations are in `message.annotations` as `url_citation` items: `start_index` and `end_index` count Unicode code points in `content`, and `title` is the URL when the title is unknown. The field is omitted when there are no citations. Match a citation to its display fields in `sources` or `page` by URL.

| `finish_reason` | Meaning |
| --- | --- |
| `stop` | The answer is complete |
| `length` | The output reached the maximum length, and the answer is cut off |
| `content_filter` | Content review refused the response. `content` is an empty string and `annotations` is omitted; `server_tool_calls` is kept, with the thinking of each step cleared. See [Model Content Safety](safety.md#handling-refusals) |

### Streaming

- Thinking and text are streamed in `delta.reasoning_content` and `delta.content` as usual. The thinking of all steps is streamed in order, without a separator.
- The progress of the tool calls is sent in `server_tool_event`, an extension field of the choice next to `delta`. A chunk carries at most one event:

| `type` | Fields | Meaning |
| --- | --- | --- |
| `step_reasoning_done` | `step` | The thinking of step `step` is complete: thinking streamed before this event and not yet assigned belongs to this step. Sent once per step, before its first call |
| `call_started` | `step`, `call` | A call of this step starts, with its complete `action` |
| `call_completed` | `step`, `call` | The call ends, with `status` and `sources`, `page` or `error`, but without `signature` |

- The complete `server_tool_calls` and `annotations` are sent once, in the `delta` of the last chunk, which carries `finish_reason`. The thinking streamed after the last `step_reasoning_done` is the thinking of the last step.
- With [`title`](conversation_title.md) enabled, the title is in `delta.title` of the last chunk, or in `message.title` of a non-streaming response.
- With the OpenAI Python SDK, the `.stream()` helper raises an error in `get_final_completion()` when the response ends with `content_filter` or `length`.

### Usage

In `usage.server_tool_use`, `tool_search`, `tool_fetch` and `tool_image_search` are the numbers of billed searches, fetches and image searches, as in the [Responses API](#responses-api).

### Multi-turn Conversations

Pass the assistant message back with `server_tool_calls` unchanged; the rules are the same as in [Multi-turn Conversations](#multi-turn). A page read from a link is restored from the `signature` of its call. If a framework or gateway drops `server_tool_calls`, the request still succeeds, but the pages read earlier are no longer in the context.
