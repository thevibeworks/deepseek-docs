---
title: "Using the Anthropic API"
description: "To meet the demand for using the Anthropic API ecosystem, our API has added support for the Anthropic API format, with the base_url being https://api.deepseek.com/anthropic."
source: https://api-docs.deepseek.com/guides/anthropic_api
fetched: 2026-10-31
---

# Using the Anthropic API

To meet the demand for using the Anthropic API ecosystem, our API has added support for the Anthropic API format, with the `base_url` being `https://api.deepseek.com/anthropic`.

With simple configuration, you can integrate the capabilities of DeepSeek into the Anthropic API ecosystem.

For request parameters, response fields, and complete HTTP examples, see the [Messages API reference](../api/create-message.md).

---

## Use DeepSeek in Claude Code

Please refer to [Integrate with Claude Code](../quick_start/agent_integrations/claude_code.md).

## Invoke DeepSeek Model via Anthropic API

1. Install Anthropic SDK

```text
pip install anthropic
```

2. Config Environment Variables

```text
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

3. Invoke the API

```text
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="deepseek-flash",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi, how are you?"
                }
            ]
        }
    ]
)
print(message.content)
```

**Note:** Unsupported model names that start with `claude` are still accepted: `claude-opus*` names are mapped to `deepseek-v4-pro`, and other `claude*` names are mapped to `deepseek-flash`. Unsupported model names that do not start with `claude` return a `400` error.

---

## Anthropic Model Mapping

When you use the Anthropic API, we map the Claude model names you pass in:

- Models starting with claude-opus are mapped to `deepseek-v4-pro`
- Models starting with claude-haiku or claude-sonnet are mapped to `deepseek-flash`

The claude-opus mapping points to `deepseek-v4-pro`, which is billed at the V4 Pro price.

With this mapping, when using the developer mode of the new Claude Desktop APP, you can bypass the APP's model name restrictions by simply changing the base\_url and api\_key to connect to DeepSeek models.

---

## Anthropic API Compatibility Details

This section lists the compatibility details of the DeepSeek API with the Anthropic API. For the full Anthropic API format definition, please refer to the [official Anthropic API reference](https://platform.claude.com/docs/en/api/python/beta/messages/create).

### HTTP Header

Authenticate with either `x-api-key: <API_KEY>` or `Authorization: Bearer <API_KEY>`.

| Field | Support Status |
| --- | --- |
| anthropic-beta | Ignored for `/messages`, except that an image with `source.type` of `file` requires `files-api-2025-04-14`; required for Files API endpoints — see [Files API](files_api.md#anthropic-compatible-files-api) |
| anthropic-version | Ignored |
| x-api-key | Fully Supported |
| Authorization | Supports `Bearer <API_KEY>` as an alternative to `x-api-key` |

### Simple Fields

| Field | Support Status |
| --- | --- |
| model | Use DeepSeek Model Instead |
| max\_tokens | Supported. Optional in HTTP requests; the default and effective limit depend on the model, thinking mode, and effort. The Anthropic SDK requires this argument, so SDK examples set it explicitly. See the compatibility exception below |
| container | Ignored |
| mcp\_servers | Ignored |
| metadata | `user_id` is supported, others are ignored Please refer to [Rate Limit & Isolation](../quick_start/rate_limit.md) for more information about `user_id` parameter. |
| service\_tier | Ignored |
| stop\_sequences | Fully Supported |
| stream | Fully Supported |
| system | Fully Supported |
| temperature | Valid range: [0.0 ~ 2.0]. Takes effect in non-thinking mode; fixed at `1.0` in thinking mode |
| thinking | Supports `type: "enabled"` and `type: "disabled"`; `adaptive` is treated as `enabled`. `budget_tokens` is ignored |
| output\_config | Only `effort` is supported |
| top\_k | Ignored |
| top\_p | Depends on the model: `deepseek-flash`: takes effect in thinking mode (lower bound `0.95`); fixed at `1.0` in non-thinking mode. `deepseek-v4-pro`: ignored in thinking mode (fixed at `0.95` when tool calling is enabled, otherwise `1.0`); takes effect in non-thinking mode. Setting `tool_choice` to `{"type": "none"}` disables tool calling even when `tools` is provided |

For certain main-agent requests from Claude Code or OpenCode in thinking mode, compatibility handling can increase the effective `max_tokens` above the requested value. In these cases, this parameter does not provide a strict output-token limit.

### Tool Fields

#### tools

For client-defined tools, provide `name`, `input_schema`, and an optional `description`, and omit `type`. The `type` field selects a server tool; passing `type: "custom"` for a client tool returns a `422` error.

| Field | Support Status |
| --- | --- |
| name | Fully Supported |
| input\_schema | Fully Supported |
| description | Fully Supported |
| cache\_control | Ignored |

#### tool\_choice

| Value | Support Status |
| --- | --- |
| none | Fully Supported |
| auto | Supported (`disable_parallel_tool_use` is ignored) |
| any | Treated as `auto`; does not force a tool call (`disable_parallel_tool_use` is ignored) |
| tool | Selects a named client tool in non-thinking mode; returns a `400` error in thinking mode (`disable_parallel_tool_use` is ignored) |

#### Returning tool results

For multi-turn conversations, send the conversation history in `messages` on every request. After an assistant message containing client `tool_use` blocks, the immediately following message must have the `user` role and include a `tool_result` for every tool call, with matching `tool_use_id` values. Place all `tool_result` blocks before any text in that user message.

When continuing tool calls in thinking mode, preserve and pass back the assistant's complete `content` array, including `thinking` and tool-use blocks. If thinking content is omitted, the service may recover it using the tool-call IDs; if recovery is required but fails, the request returns a `400` error. Do not rely on automatic recovery.

### Message Fields

| Field | Variant | Sub-Field | Support Status |
| --- | --- | --- | --- |
| content | string |  | Fully Supported |
| array, type="text" | text | Fully Supported |
| cache\_control | Ignored |
| citations | Ignored |
| array, type="image" | source | `deepseek-flash` supports images in user messages and `tool_result` content; images in assistant messages return a `400` error. `deepseek-v4-pro` does not process images and replaces them with the text `[Unsupported Image]`. `source.type` can be base64 (media types: image/jpeg, image/png, image/gif, image/webp), url, or file (include the header `anthropic-beta: files-api-2025-04-14` when using file images). |
| array, type = "document" |  | Not Supported |
| array, type = "search\_result" |  | Not Supported |
| array, type = "thinking" |  | Supported |
| array, type="redacted\_thinking" |  | Not Supported |
| array, type = "tool\_use" | id | Fully Supported |
| input | Fully Supported |
| name | Fully Supported |
| cache\_control | Ignored |
| array, type = "tool\_result" | tool\_use\_id | Fully Supported |
| content | Fully Supported |
| cache\_control | Ignored |
| is\_error | Ignored |
| array, type = "server\_tool\_use" |  | Supported |
| array, type = "web\_search\_tool\_result" |  | Supported |
| array, type = "code\_execution\_tool\_result" |  | Not Supported |
| array, type = "mcp\_tool\_use" |  | Not Supported |
| array, type = "mcp\_tool\_result" |  | Not Supported |
| array, type = "container\_upload" |  | Not Supported |

## Server tool usage

A content block with `type: "server_tool_use"` describes a tool call executed by the service. It contains the call `id`, tool `name`, JSON `input`, and `caller`. For web search, `name` is `web_search`, `input` contains the search `query`, and `caller` is `{"type":"direct"}`. The matching `web_search_tool_result` block uses the same ID in `tool_use_id`. The service runs the search and continues generating the answer; the client does not need to execute the tool or supply a `tool_result`.

`usage.server_tool_use` reports request-level counters for these searches:

| Field | Meaning |
| --- | --- |
| `web_search_requests` | Number of attempted server-side web searches, including attempts rejected for exceeding `max_uses`, invalid queries, and failed searches. It can therefore exceed `max_uses`. |
| `tool_search` | Number of web searches that succeeded and returned at least one result. A failed search or an empty result does not increment this counter. It counts calls, not individual search results. |

The object is omitted when no web search was attempted; declaring a search tool in `tools` does not guarantee that it appears. For a non-streaming response, read `usage.server_tool_use`. For streaming, read the cumulative counters in the final `message_delta.usage.server_tool_use`; the initial `message_start` usage does not contain them.

For example, send this request body to `POST /anthropic/v1/messages` with your DeepSeek API key:

```json
{
  "model": "deepseek-v4-pro",
  "max_tokens": 256,
  "thinking": {"type": "disabled"},
  "tools": [
    {"type": "web_search_20250305", "name": "web_search", "max_uses": 1}
  ],
  "messages": [
    {
      "role": "user",
      "content": "Use the web search tool once to search for Python official website. Then reply with only the official site URL."
    }
  ]
}
```

A successful response to this request contained `server_tool_use`, `web_search_tool_result`, and `text` content blocks, with the following usage. Token counts and search counts can vary between requests.

```json
{
  "usage": {
    "input_tokens": 2912,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 256,
    "output_tokens": 52,
    "service_tier": "standard",
    "server_tool_use": {
      "web_search_requests": 1,
      "tool_search": 1
    }
  }
}
```

## Streaming and token usage

Set `stream` to `true` to receive server-sent events (SSE). A normal response starts with `message_start`, emits `content_block_start`, `content_block_delta`, and `content_block_stop` for its content blocks, then ends with `message_delta` and `message_stop`. `ping` events may appear between these events. The stream does not send `data: [DONE]`.

Normal message events have an SSE `event` name and a JSON `type` field. Keep-alive comments may also appear. If waiting for generation to start times out, the service may send an unnamed `data` frame containing `{"error":{"message":"..."}}`, without an SSE `event` name or a top-level JSON `type`, and then close the connection. A connection that closes before `message_stop` indicates an incomplete response.

Use the final `message_delta.usage` as the request's token usage; do not add it to the initial usage in `message_start`. `input_tokens` excludes cache hits, `cache_read_input_tokens` reports cache hits, and `cache_creation_input_tokens` is currently `0`. The total input token count is `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`.

See the [Messages API reference](../api/create-message.md) for response examples and error handling.
