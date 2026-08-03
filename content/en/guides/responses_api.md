---
title: "Using the Responses API"
description: "The Responses API currently only supports the deepseek-v4-flash model, and does not yet support the deepseek-v4-pro model. We will add support for the deepseek-v4-pro model in early August 2026."
source: https://api-docs.deepseek.com/guides/responses_api
fetched: 2026-08-02
---

# Using the Responses API

Supported Models

The Responses API currently only supports the `deepseek-v4-flash` model, and does not yet support the `deepseek-v4-pro` model. We will add support for the `deepseek-v4-pro` model in early August 2026.

To meet the demand for Codex, our API now supports the Responses API format, with the base\_url `https://api.deepseek.com`.

With a simple configuration, you can use DeepSeek models in Codex.

## Integrating DeepSeek Models into Codex

Please refer to [Integrate with Codex](../quick_start/agent_integrations/codex.md).

## Calling DeepSeek Models via the Responses API

```python
# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="<your DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.responses.create(
    model="deepseek-v4-flash",
    instructions="You are a helpful assistant.",
    input="Hi, how are you?",
)

print(response.output_text)
```

## Streaming

Set `stream: true` to receive the response as a sequence of semantic server-sent events (SSE). Each event carries an `event` field indicating the event type, and a monotonically increasing `sequence_number`. The stream ends with a `response.completed` / `response.incomplete` / `response.failed` event — there is no `data: [DONE]` message.

```python
stream = client.responses.create(
    model="deepseek-v4-flash",
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
| `response.output_item.added` / `response.output_item.done` | An output item (`reasoning` / `message` / `function_call` / `custom_tool_call` / `web_search_call`) starts / completes |
| `response.content_part.added` / `response.content_part.done` | A content part within an output item starts / completes |
| `response.reasoning_text.delta` / `response.reasoning_text.done` | Incremental chain-of-thought text / the full chain-of-thought text |
| `response.output_text.delta` / `response.output_text.done` | Incremental output text / the full output text |
| `response.function_call_arguments.delta` / `response.function_call_arguments.done` | Incremental function call arguments / the full arguments |
| `response.custom_tool_call_input.delta` / `response.custom_tool_call_input.done` | Incremental custom tool call (`apply_patch`) input / the full input |
| `response.web_search_call.in_progress` / `response.web_search_call.searching` / `response.web_search_call.completed` | Status updates of a server-side web search tool call |
| `response.completed` | The final event when the response completes normally, carrying the full `response` object including `usage` |
| `response.incomplete` | The final event when the response is truncated (e.g. reaching `max_output_tokens`), carrying the full `response` object |
| `response.failed` | The final event when the response fails, carrying the full `response` object with `error` details |

## Compatibility Details

This section lists the compatibility details of the DeepSeek API with the Responses API. For the full Responses API format definition, please refer to the [official OpenAI API reference](https://developers.openai.com/api/reference/resources/responses/methods/create).

### Top-level Request Parameters

| Parameter | Support Status |
| --- | --- |
| `model` | Supported. Currently only `deepseek-v4-flash` (`deepseek-v4-pro` is not supported yet), see [Models & Pricing](../quick_start/pricing.md) |
| `input` | Supported. String or input item list; at least one of `input` and `instructions` is required |
| `instructions` | Supported. Inserted as the first system message |
| `stream` | Supported |
| `temperature` | Supported (range [0.0, 2.0]; no effect in thinking mode) |
| `top_p` | Supported (no effect in thinking mode) |
| `max_output_tokens` | Supported |
| `top_logprobs` | Supported (range [0, 20]) |
| `tools` | Partially supported. `function` / `web_search` supported; other types ignored, see the Tools table below |
| `tool_choice` | Supported. `none` / `auto` / `required` / a specific tool (`{"type": "function", "name": ...}` or `{"type": "web_search"}` / `{"type": "web_search_2025_08_26"}`) |
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
| `message` | Supported. Roles `user` / `assistant` / `system` / `developer` (`developer` is treated as `system`); content supports strings and `input_text` / `output_text` content parts. Image and file inputs are not supported (`input_image` parts do not cause an error, but are replaced with a placeholder text) |
| `function_call` | Supported. Merged into the adjacent assistant message |
| `function_call_output` | Supported |
| `reasoning` | Supported. Plain-text `content` is merged into the adjacent assistant message; `summary` and `encrypted_content` are not supported |
| `web_search_call` | Supported. Pass back as-is; the server automatically restores the search results |
| Other types | Ignored |

### Tools

| Type | Support Status |
| --- | --- |
| `function` | Supported |
| `web_search` / `web_search_2025_08_26` | Supported, executed on the server side. `search_context_size` and `user_location` are ignored |
| `custom` | Only `{"type": "custom", "name": "apply_patch"}` is supported (for Codex compatibility); other names return a `400` error |
| `file_search` / `code_interpreter` / `computer_use` / `mcp` / other built-in tools | Ignored |

### Response Fields

The response object is compatible with the OpenAI Responses API `response` structure. Fields that depend on unsupported capabilities always take fixed values (e.g. `store: false`, `previous_response_id: null`, `parallel_tool_calls: true`).

Token usage is returned in `usage`:

- `input_tokens`: number of input tokens, where `input_tokens_details.cached_tokens` is the number of tokens hitting the [context cache](kv_cache.md)
- `output_tokens`: number of output tokens, where `output_tokens_details.reasoning_tokens` is the number of chain-of-thought tokens
