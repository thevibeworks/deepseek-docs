---
title: "Using the Responses API"
description: "To meet the demand for Codex, our API now supports the Responses API format, with the base_url being https://api.deepseek.com."
source: https://api-docs.deepseek.com/guides/responses_api
fetched: 2026-10-31
---

# Using the Responses API

To meet the demand for Codex, our API now supports the Responses API format, with the `base_url` being `https://api.deepseek.com`.

With a simple configuration, you can use DeepSeek models in Codex.

## Integrating DeepSeek Models into Codex

Please refer to [Integrate with Codex](../quick_start/agent_integrations/codex.md).

## Calling DeepSeek Models via the Responses API

```python
# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="<your DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.responses.create(
    model="deepseek-flash",
    instructions="You are a helpful assistant.",
    input="Hi, how are you?",
)

print(response.output_text)
```

## Streaming

Set `stream: true` to receive the response as a sequence of semantic server-sent events (SSE). Each event carries an `event` field indicating the event type, and a monotonically increasing `sequence_number`. The stream ends with a `response.completed` / `response.incomplete` / `response.failed` event — there is no `data: [DONE]` message.

```python
stream = client.responses.create(
    model="deepseek-flash",
    instructions="You are a helpful assistant.",
    input="Hi, how are you?",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
```

The full list of events:

| Event | Description |
| --- | --- |
| `response.created` | The first event; the response has been created with status `in_progress` |
| `response.in_progress` | The response is being generated |
| `response.output_item.added` / `response.output_item.done` | An output item (`reasoning` / `message` / `function_call` / `custom_tool_call` / `web_search_call` / `tool_search_call`) starts / completes |
| `response.content_part.added` / `response.content_part.done` | A content part within an output item starts / completes |
| `response.reasoning_text.delta` / `response.reasoning_text.done` | Incremental chain-of-thought text / the full chain-of-thought text |
| `response.output_text.delta` / `response.output_text.done` | Incremental output text / the full output text |
| `response.function_call_arguments.delta` / `response.function_call_arguments.done` | Incremental function call arguments / the full arguments |
| `response.custom_tool_call_input.delta` / `response.custom_tool_call_input.done` | Incremental custom tool call (`apply_patch`) input / the full input |
| `response.web_search_call.in_progress` / `response.web_search_call.searching` / `response.web_search_call.completed` | A server-side `web_search` call starts / is running / completes (`deepseek-v4-pro` only) |
| `response.completed` | The final event when the response completes normally, carrying the full `response` object including `usage` |
| `response.incomplete` | The final event when the response is truncated (e.g. reaching `max_output_tokens`), carrying the full `response` object |
| `response.failed` | The final event when the response fails, carrying the full `response` object with `error` details |

## Image Input

The Responses API accepts images with the `deepseek-flash` model. The same image limits and supported formats as [Chat Completions](vision.md#limits) apply.

Images are provided via an `input_image` content part in a `message` item, with either `image_url` (an `http(s)` URL or a base64 data URL) or `file_id` (an image uploaded via the [Files API](files_api.md)):

```python
response = client.responses.create(
    model="deepseek-flash",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image?"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg", "detail": "low"},
            ],
        },
    ],
)
print(response.output_text)
```

`input_image` parts may also appear in the `output` of `function_call_output` / `custom_tool_call_output` items, so the model can receive images produced by your tools:

```python
input=[
    {"role": "user", "content": "Read the screenshot the tool returned."},
    {"type": "function_call", "call_id": "fc1", "name": "take_screenshot", "arguments": "{}"},
    {"type": "function_call_output", "call_id": "fc1",
     "output": [{"type": "input_image", "image_url": "data:image/png;base64,<BASE64_DATA>"}]},
]
```

### `input_image` Fields

- `image_url`: An `http(s)` URL (at most 8192 characters) or a base64-encoded data URL (`data:image/jpeg;base64,...`). Supported formats: JPEG, PNG, GIF, WebP.
- `file_id`: The ID of an image uploaded via the [Files API](files_api.md), of the form `file-api-...`.
- `detail`: `low` / `high` / `original` / `auto`. `low` downsamples the image to 512x512 before inference; the other values keep the original image. Ignored when `file_id` is set.

`image_url` and `file_id` are mutually exclusive: passing neither returns a `400` error ("input\_image must have image\_url or file\_id"), and passing both returns a `400` error ("input\_image cannot have both image\_url and file\_id").

### Restrictions

- Images are allowed only in `user` / `developer` message items and in `function_call_output` / `custom_tool_call_output` outputs. Images in `system` or `assistant` messages return a `400` error.
- `deepseek-flash` processes `input_image` parts as real images.
- The same shared image limits as Chat Completions apply (32 MiB per inline image, 64 MiB per `file_id` image, 64 MiB total without `file_id` images or up to 200 MiB with them, 600 images per request, etc.) — see [Vision: Limits](vision.md#limits).

## Compatibility Details

This section lists the compatibility details of the DeepSeek API with the Responses API. For the full Responses API format definition, please refer to the [official OpenAI API reference](https://developers.openai.com/api/reference/resources/responses/methods/create).

### Top-level Request Parameters

| Parameter | Support Status |
| --- | --- |
| `model` | Supported. `deepseek-flash` and `deepseek-v4-pro`, see [Models & Pricing](../quick_start/pricing.md) |
| `input` | Supported. String or input item list; at least one of `input` and `instructions` is required |
| `instructions` | Supported. Inserted as the first system message |
| `stream` | Supported |
| `temperature` | Supported (range [0.0, 2.0]; no effect in thinking mode) |
| `top_p` | Supported; behavior depends on the model: `deepseek-flash`: takes effect in thinking mode (lower bound `0.95`); fixed at `1.0` in non-thinking mode. `deepseek-v4-pro`: ignored in thinking mode (fixed at `0.95` when tool calling is enabled, otherwise `1.0`); takes effect in non-thinking mode. Setting `tool_choice` to `none` disables tool calling even when `tools` is provided |
| `max_output_tokens` | Supported |
| `top_logprobs` | Supported (range [0, 20]) |
| `tools` | Partially supported. `function` supported; `web_search` supported with `deepseek-v4-pro`; other types ignored, see the Tools table below |
| `tool_choice` | Supported. `none` / `auto` / `required` / a specific tool (`{"type": "function", "name": ...}`) |
| `reasoning` | Partially supported. `effort` supported; `summary` accepted but no summary is generated |
| `text` | Partially supported. `format` fully supported; `verbosity` accepted but has no effect |
| `user` | Supported. See [Rate Limit & Isolation](../quick_start/rate_limit.md) |
| `parallel_tool_calls` | Ignored (parallel tool calling is always enabled) |
| `max_tool_calls` | Ignored |
| `previous_response_id` | Not supported (stateless API) |
| `conversation` | Not supported (stateless API) |
| `store` | Not supported. The response always carries `store: false` |
| `background` | Not supported |
| `metadata` | Not supported |
| `include` | Not supported |
| `prompt` | Not supported |
| `truncation` | Not supported. Requests exceeding the context window return a `400` error |
| `service_tier` | Not supported |
| `safety_identifier` | Not supported |
| `prompt_cache_key` / `prompt_cache_retention` | Not supported. Context caching is managed automatically, see [Context Caching](kv_cache.md) |
| `context_management` | Not supported |
| `stream_options` | Not supported |

Unsupported parameters are **silently ignored** and do not cause errors, so existing Responses API clients can connect without modification.

### Input Items

| Type | Support Status |
| --- | --- |
| `message` | Supported. Roles `user` / `assistant` / `system` / `developer` (`developer` is treated as `user`); content supports strings and `input_text` / `output_text` / `input_image` content parts. `input_image` parts are processed as real images (allowed in `user` / `developer` messages only; images in `system` / `assistant` messages return a `400` error). File inputs are not supported |
| `function_call` | Supported. Merged into the adjacent assistant message |
| `function_call_output` | Supported. The `output` may be a string or a list of content parts; `input_image` parts in the output are processed as real images |
| `reasoning` | Supported. Plain-text `content` is merged into the adjacent assistant message; `summary` and `encrypted_content` are not supported |
| `custom_tool_call` / `custom_tool_call_output` | Supported (for the `apply_patch` custom tool, with `call_id` pairing validation). `input_image` parts in the `output` are processed as real images |
| Other types | Ignored |

Note: `web_search_call` items returned by a previous response can be passed back in `input`; their search results are restored and concatenated into the context.

### Tools

| Type | Support Status |
| --- | --- |
| `function` | Supported |
| `custom` | Only `{"type": "custom", "name": "apply_patch"}` is supported (for Codex compatibility); other names return a `400` error |
| `web_search` | Supported with `deepseek-v4-pro`. The API runs the search on the server, adds the results to the context, and continues the response. Ignored with `deepseek-flash` |
| `file_search` / `code_interpreter` / `computer_use` / `mcp` / other built-in tools | Ignored |

### Response Fields

The response object is compatible with the OpenAI Responses API `response` structure. Fields that depend on unsupported capabilities always take fixed values (e.g. `store: false`, `previous_response_id: null`, `parallel_tool_calls: true`).

Token usage is returned in `usage`:

- `input_tokens`: number of input tokens, where `input_tokens_details.cached_tokens` is the number of tokens hitting the [context cache](kv_cache.md)
- `output_tokens`: number of output tokens, where `output_tokens_details.reasoning_tokens` is the number of chain-of-thought tokens

#### Server Tool Usage

When server-side web tools complete successfully, `usage.server_tool_use` reports their usage for the entire response:

| Field | Meaning |
| --- | --- |
| `tool_search` | Number of successful web search queries. A search call containing multiple queries can contribute more than one to this count |
| `tool_fetch` | Number of successful web page reads, including opening a page and finding text within a page |

These values count tool operations, not tokens. `tool_search` counts web searches; it does not count client-side tool discovery represented by `tool_search_call` output items. Failed operations are not counted, and searches returning no results do not increase `tool_search`. If both counts are zero, the entire `server_tool_use` field is omitted. When the field is present, both counts are included, even if one is zero.

The `web_search_call` items in `output` describe individual server-side operations; `usage.server_tool_use` contains the aggregate counts. For streaming requests, read these counts from `response.usage` in the final `response.completed`, `response.incomplete`, or `response.failed` event. They are not sent as a separate usage event, and `usage` is `null` in the initial response events.

For example, this request enables web search with `deepseek-v4-pro`. Omitting `tool_choice` uses the default automatic selection:

```json
{
  "model": "deepseek-v4-pro",
  "max_output_tokens": 256,
  "reasoning": {"effort": "none"},
  "tools": [{"type": "web_search"}],
  "input": "Use the web search tool once to search for Python official website. Then reply with only the official site URL."
}
```

The following usage excerpt shows one successful search and no page reads. Token and tool counts can vary between requests:

```json
{
  "usage": {
    "input_tokens": 3475,
    "input_tokens_details": {"cached_tokens": 512},
    "output_tokens": 54,
    "output_tokens_details": {"reasoning_tokens": 0},
    "total_tokens": 3529,
    "server_tool_use": {
      "tool_search": 1,
      "tool_fetch": 0
    }
  }
}
```
