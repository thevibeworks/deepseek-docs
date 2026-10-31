---
title: "Responses API"
description: "Creates a model response in the OpenAI Responses API format."
source: https://api-docs.deepseek.com/api/create-response
fetched: 2026-10-31
---

# Responses API

[Open Markdown](https://api-docs.deepseek.com/api/create-response.md "Open Markdown in a new tab")

```
POST /responses
```

Creates a model response in the OpenAI Responses API format.

The API is **stateless**: responses and conversations are not stored on the server. For multi-turn conversations, the client needs to send the full conversation history in `input` on each request. Please refer to the [Responses API Guide](../guides/responses_api.md) for details, including the full parameter compatibility tables.

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** `deepseek-flash`, `deepseek-v4-pro`

ID of the model to use. Use `deepseek-flash` or `deepseek-v4-pro`.

**input** string | object[]

nullable

The input to the model. Either a plain string (treated as a single `user` message), or a list of input items.

Supported input item types are `message` / `function_call` / `function_call_output` / `custom_tool_call` / `custom_tool_call_output` / `reasoning` / `web_search_call`; other types are ignored. Message roles can be `user` / `assistant` / `system` / `developer` (`developer` is treated as `user`). With the `deepseek-flash` model, `input_image` content parts are supported in `user` / `developer` message items and in the `output` of `function_call_output` / `custom_tool_call_output` items; images in `system` or `assistant` messages return a `400` error. File inputs are not supported.

At least one of `input` and `instructions` is required.

oneOf

- Text input
- Input item list

**[Text input]**

string

**[Input item list]**

An input item. Supported types are `message` / `function_call` / `function_call_output` / `custom_tool_call` / `custom_tool_call_output` / `reasoning` / `web_search_call`; other types are ignored. `reasoning` and `function_call` items are automatically merged into the adjacent assistant message by the server. A `web_search_call` item returned by a previous response can be passed back to restore its search results into the context. Please refer to the [Responses API Guide](../guides/responses_api.md#multi-turn-conversation) for the pass-back rules in multi-turn conversations.

- Array [

**type** string

**Possible values:** `message`, `function_call`, `function_call_output`, `custom_tool_call`, `custom_tool_call_output`, `reasoning`, `web_search_call`

The type of the input item. For `message` items, this field can be omitted if `role` is present. `custom_tool_call` / `custom_tool_call_output` items are used together with the `apply_patch` custom tool. `web_search_call` items restore the search results of a previous server-side search.

**role** string

**Possible values:** `user`, `assistant`, `system`, `developer`

For `message` items. The role of the message author. `developer` is treated as `user`.

**content** string | object[]

For `message` items, the message content, either a plain string or a list of `input_text` / `output_text` / `input_image` content parts. For `reasoning` items, a list of `reasoning_text` content parts.

oneOf

- Text content
- Array of content parts

**[Text content]**

string

**[Array of content parts]**

- Array [

oneOf

- Text content part
- Image content part
- Reasoning text content part

**[Text content part]**

**type** stringrequired

**Possible values:** `input_text`, `output_text`

The type of the content part.

**text** stringrequired

The text content.

**[Image content part]**

An image content part. Processed as a real image. Allowed only in `user` / `developer` message items and in the `output` of `function_call_output` / `custom_tool_call_output` items; images in `system` or `assistant` messages return a `400` error ("Image in system message is unsupported" / "Image in assistant message is unsupported").

**type** stringrequired

**Possible values:** `input_image`

The type of the content part, in this case `input_image`.

**image\_url** string

The image source, either an `http(s)` URL of the image (max 8192 characters) or a base64-encoded data URL (`data:image/jpeg;base64,...`). Supported formats: JPEG, PNG, GIF, and WebP. Mutually exclusive with `file_id`: passing neither returns a `400` error ("input\_image must have image\_url or file\_id"); passing both returns a `400` error ("input\_image cannot have both image\_url and file\_id").

**detail** string

**Possible values:** `low`, `high`, `original`, `auto`

Controls how the image is processed. `low` downsamples the image to 512x512 (faster, cheaper). `high`, `original`, and `auto` keep the original image. Ignored when `file_id` is set.

**file\_id** string

The ID of an image file uploaded via the [Files API](../guides/files_api.md), of the form `file-api-...`. Mutually exclusive with `image_url`; `detail` is ignored when `file_id` is set.

**[Reasoning text content part]**

**type** stringrequired

**Possible values:** `reasoning_text`

The type of the content part, in this case `reasoning_text`.

**text** stringrequired

The chain-of-thought text content.

- ]

**call\_id** string

For `function_call` / `function_call_output` items. The ID pairing a function call with its output. Must be non-empty and unique, and every `function_call` must have a matching `function_call_output`.

**name** string

For `function_call` items. The name of the function to call.

**arguments** string

For `function_call` items. The arguments to call the function with, in JSON format.

**output** string | object[]

For `function_call_output` / `custom_tool_call_output` items. The output of the tool call, either a plain string or a list of `input_text` / `input_image` content parts.

oneOf

- Text output
- Array of content parts

**[Text output]**

string

**[Array of content parts]**

- Array [

oneOf

- Text content part
- Image content part
- Reasoning text content part

**[Text content part]**

**type** stringrequired

**Possible values:** `input_text`, `output_text`

The type of the content part.

**text** stringrequired

The text content.

**[Image content part]**

An image content part. Processed as a real image. Allowed only in `user` / `developer` message items and in the `output` of `function_call_output` / `custom_tool_call_output` items; images in `system` or `assistant` messages return a `400` error ("Image in system message is unsupported" / "Image in assistant message is unsupported").

**type** stringrequired

**Possible values:** `input_image`

The type of the content part, in this case `input_image`.

**image\_url** string

The image source, either an `http(s)` URL of the image (max 8192 characters) or a base64-encoded data URL (`data:image/jpeg;base64,...`). Supported formats: JPEG, PNG, GIF, and WebP. Mutually exclusive with `file_id`: passing neither returns a `400` error ("input\_image must have image\_url or file\_id"); passing both returns a `400` error ("input\_image cannot have both image\_url and file\_id").

**detail** string

**Possible values:** `low`, `high`, `original`, `auto`

Controls how the image is processed. `low` downsamples the image to 512x512 (faster, cheaper). `high`, `original`, and `auto` keep the original image. Ignored when `file_id` is set.

**file\_id** string

The ID of an image file uploaded via the [Files API](../guides/files_api.md), of the form `file-api-...`. Mutually exclusive with `image_url`; `detail` is ignored when `file_id` is set.

**[Reasoning text content part]**

**type** stringrequired

**Possible values:** `reasoning_text`

The type of the content part, in this case `reasoning_text`.

**text** stringrequired

The chain-of-thought text content.

- ]

- ]

**instructions** stringnullable

A system-level instruction, inserted as the first system message of the model's context.

**reasoning**

object

nullable

Configuration of the thinking mode.

**effort** string

**Possible values:** `none`, `low`, `high`, `max`

Controls the thinking mode toggle and the thinking effort. `none` disables thinking mode; `low` / `high` / `max` enable thinking mode. If not set, the model's default thinking behavior is used (enabled by default). For compatibility with existing software, `minimal` is accepted and mapped to `low`, and `medium` / `xhigh` are accepted and mapped to `high`.

**max\_output\_tokens** integernullable

An upper bound for the number of tokens that can be generated in the response, including both the visible output tokens and the reasoning tokens.

**stream** booleannullable

**Default value:** `false`

If set to `true`, the response is streamed as semantic server-sent events. The final event is `response.completed` / `response.incomplete` / `response.failed` (there is no `data: [DONE]` message). Please refer to the [Responses API Guide](../guides/responses_api.md#streaming) for the full event list.

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Has no effect in thinking mode.

**top\_p** numbernullable

**Possible values:** `>= 0` and `<= 1`

An alternative to sampling with temperature, called nucleus sampling. The effective value depends on the model and mode:

- `deepseek-flash`: In thinking mode, the default is 1.0 and values below 0.95 are treated as 0.95. In non-thinking mode, it is fixed at 1.0 and the value you pass is ignored.
- `deepseek-v4-pro`: In thinking mode, it is fixed at 0.95 when tool calling is enabled, or 1.0 otherwise; the value you pass is ignored. Setting `tool_choice` to `none` disables tool calling even when `tools` is provided. In non-thinking mode, the value you pass is used, with a default of 1.0.

**text**

object

nullable

Configuration of the text output.

**format**

object

The output format. `{"type": "text"}` (default) for plain text; `{"type": "json_object"}` for JSON mode; `{"type": "json_schema", "name": ..., "schema": ...}` for structured output conforming to the given JSON Schema.

If `text` is omitted or `null`, or `format` is omitted, plain text is used. When a `format` object is provided, `type` is required.

**type** stringrequired

**Possible values:** `text`, `json_object`, `json_schema`

**name** string

The name of the schema. Required when `type` is `json_schema`.

**schema** object

The JSON Schema that the output must conform to. Required when `type` is `json_schema`.

**tools**

object[]

nullable

A list of tools the model may call. Function names must be non-empty, at most 128 characters, match `^[a-zA-Z0-9_-]+$`, and be unique across all tools. `function` tools are supported; `web_search` is supported with `deepseek-v4-pro`; other built-in tool types are ignored. Please refer to the [Responses API Guide](../guides/responses_api.md) for details.

A tool the model may call. `function` defines a function tool — note that in the Responses API format, `name` / `parameters` and other function fields are at the top level of the tool object. `custom` defines a custom tool; only `{"type": "custom", "name": "apply_patch"}` is supported, and other names return a `400` error. `web_search` enables server-side web search and is supported with `deepseek-v4-pro`.

- Array [

**type** stringrequired

**Possible values:** `function`, `custom`, `web_search`

The type of the tool: `function`, `custom` (only `apply_patch`), or `web_search` (`deepseek-v4-pro` only).

**name** string

For `function` and `custom` tools. The name of the tool. For function tools, must be non-empty, at most 128 characters, match `^[a-zA-Z0-9_-]+$`, and be unique across all tools. For custom tools, must be `apply_patch`.

**description** string

For `function` tools. A description of what the function does, used by the model to choose when and how to call the function.

**parameters**

object

The parameters the functions accepts, described as a JSON Schema object. See the [Tool Calls Guide](../guides/tool_calls.md) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

**property name\*** anynullable

- ]

**tool\_choice** string | object

nullable

Controls which (if any) tool is called by the model.

`none` means the model will not call any tool and instead generates a message.

`auto` (default) means the model can pick between generating a message or calling one or more tools.

`required` means the model must call one or more tools.

Specifying a particular tool via `{"type": "function", "name": "my_function"}` forces the model to call that tool.

oneOf

- Tool choice mode
- Named tool choice

**[Tool choice mode]**

string

**Possible values:** `none`, `auto`, `required`

**[Named tool choice]**

Forces the model to call the specified tool. `name` is required when `type` is `function`.

**type** stringrequired

**Possible values:** `function`

**name** string

The name of the function to call. Required when `type` is `function`.

**top\_logprobs** integernullable

**Possible values:** `>= 0` and `<= 20`

**Default value:** `null`

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

**user** stringnullable

A custom end-user identifier. We recommend using only ASCII letters, digits, underscores (`_`), and hyphens (`-`). The UTF-8 encoded value must not exceed 512 bytes. Do not include user privacy information.

- It can be used to distinguish user identities on your side to help us with content safety review, for KVCache isolation, and for scheduling isolation. For more details, please refer to [Rate Limit & Isolation](../quick_start/rate_limit.md)

## Responses

- 200 (No streaming)
- 200 (Streaming)

OK, returns a `response` object

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

A unique identifier for the response.

**object** stringrequired

**Possible values:** `response`

The object type, which is always `response`.

**created\_at** integerrequired

The Unix timestamp (in seconds) of when the response was created.

**status** stringrequired

**Possible values:** `in_progress`, `completed`, `incomplete`, `failed`

The status of the response.

**error** objectnullable

The error object when the response failed, with `code` and `message` fields.

**incomplete\_details**

object

nullable

The details about why the response is incomplete. The `reason` field can be `max_output_tokens` or `content_filter`.

**reason** string

**Possible values:** `max_output_tokens`, `content_filter`

**model** stringrequired

The model used for the response.

**output**

object[]

required

The list of output items generated by the model. In thinking mode, the chain-of-thought is returned as a `reasoning` item before the `message` item. Function calls are returned as `function_call` items.

An output item generated by the model. `message` items carry the assistant text, `reasoning` items carry the chain-of-thought, `function_call` items represent function calls, `custom_tool_call` items represent custom tool calls (such as `apply_patch`), `web_search_call` items represent server-side web searches (`deepseek-v4-pro` only), and `tool_search_call` items represent tool searches.

- Array [

**type** string

**Possible values:** `message`, `reasoning`, `function_call`, `custom_tool_call`, `web_search_call`, `tool_search_call`

The type of the output item: `message` / `reasoning` / `function_call` / `custom_tool_call` / `web_search_call` / `tool_search_call`.

**id** string

The unique ID of the output item.

**status** string

**Possible values:** `in_progress`, `completed`, `incomplete`

The status of the output item.

**role** string

**Possible values:** `assistant`

For `message` items. Always `assistant`.

**content**

object[]

For `message` items, a list of `output_text` content parts. For `reasoning` items, a list of `reasoning_text` content parts carrying the chain-of-thought in plain text.

- Array [

**type** string

**Possible values:** `output_text`, `reasoning_text`

**text** string

- ]

**call\_id** string

For `function_call` / `custom_tool_call` / `tool_search_call` items. An identifier used when passing the tool output back to the API.

**name** string

For `function_call` / `custom_tool_call` items. The name of the function or custom tool to call.

**arguments** string

For `function_call` items. The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

- ]

**usage**

object

nullable

Token and server-tool usage statistics for the response. Null in initial streaming events; read usage from the final response.

**input\_tokens** integerrequired

Number of input tokens.

**input\_tokens\_details**

object

Breakdown of the input tokens.

**cached\_tokens** integer

Number of input tokens that hit the context cache. See [Context Caching](../guides/kv_cache.md).

**output\_tokens** integerrequired

Number of output tokens.

**output\_tokens\_details**

object

Breakdown of the output tokens.

**reasoning\_tokens** integer

Number of reasoning (chain-of-thought) tokens generated by the model.

**total\_tokens** integerrequired

Total number of tokens used in the request (input + output).

**server\_tool\_use**

object

Successful server-side web search and page-fetch counts, separate from token usage. Present only when tool\_search or tool\_fetch is greater than zero; otherwise omitted. Both fields are present when this object is returned. In streaming responses, read response.usage from the terminal response.completed, response.incomplete, or response.failed event. These are cumulative counts, not deltas. See [Server tool usage](../guides/responses_api.md#server-tool-usage).

**tool\_search** integerrequired

**Possible values:** `>= 0`

Number of successful web search queries. A search with multiple queries can add more than one; failed queries and queries with no results are not counted. This field can be used as a basis for billing.

**tool\_fetch** integerrequired

**Possible values:** `>= 0`

Number of successful page fetches performed by open\_page or find\_in\_page. Failed attempts are not counted. This field can be used as a basis for billing.

**[Example]**

```json
{
  "id": "387b53c1-7ad2-4259-9298-61b139f5bd20",
  "object": "response",
  "created_at": 1793084842,
  "status": "completed",
  "background": false,
  "completed_at": 1793084843,
  "content_filters": null,
  "error": null,
  "frequency_penalty": 0.0,
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": 32,
  "max_tool_calls": null,
  "model": "deepseek-flash",
  "moderation": null,
  "output": [
    {
      "type": "message",
      "id": "4e706f35-6ea2-468a-bd19-a9c1adc54726",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "Hello! 👋 How can I help you today?"
        }
      ],
      "phase": "final_answer",
      "role": "assistant"
    }
  ],
  "parallel_tool_calls": true,
  "presence_penalty": 0.0,
  "previous_response_id": null,
  "prompt_cache_key": null,
  "prompt_cache_retention": null,
  "reasoning": {
    "effort": "none",
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "store": false,
  "temperature": 1.0,
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": null
  },
  "tool_choice": "auto",
  "tools": [],
  "top_logprobs": 0,
  "top_p": 1.0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 7,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 11,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 18
  },
  "user": null,
  "metadata": {}
}
```

OK, returns a streamed sequence of semantic server-sent events. Each event has an `event` field for the event type and an incrementing `sequence_number`. The final event is `response.completed` / `response.incomplete` / `response.failed` (there is no `data: [DONE]` message). Please refer to the [Responses API Guide](../guides/responses_api.md#streaming) for the full event list.

**[text/event-stream]**

- Schema
- Example

**[Schema]**

**Schema**

- Array [

object

- ]

**[Example]**

```shell
event: response.created
data: {"type":"response.created","response":{"id":"19460ef2-58da-46c5-9510-9e7b04c47e4a","object":"response","created_at":1793084908,"status":"in_progress","background":false,"completed_at":null,"content_filters":null,"error":null,"frequency_penalty":0.0,"incomplete_details":null,"instructions":null,"max_output_tokens":32,"max_tool_calls":null,"model":"deepseek-flash","moderation":null,"output":[],"parallel_tool_calls":true,"presence_penalty":0.0,"previous_response_id":null,"prompt_cache_key":null,"prompt_cache_retention":null,"reasoning":{"effort":"none","summary":null},"safety_identifier":null,"service_tier":"default","store":false,"temperature":1.0,"text":{"format":{"type":"text"},"verbosity":null},"tool_choice":"auto","tools":[],"top_logprobs":0,"top_p":1.0,"truncation":"disabled","usage":null,"user":null,"metadata":{}},"sequence_number":0}

event: response.in_progress
data: {"type":"response.in_progress","response":{"id":"19460ef2-58da-46c5-9510-9e7b04c47e4a","object":"response","created_at":1793084908,"status":"in_progress","background":false,"completed_at":null,"content_filters":null,"error":null,"frequency_penalty":0.0,"incomplete_details":null,"instructions":null,"max_output_tokens":32,"max_tool_calls":null,"model":"deepseek-flash","moderation":null,"output":[],"parallel_tool_calls":true,"presence_penalty":0.0,"previous_response_id":null,"prompt_cache_key":null,"prompt_cache_retention":null,"reasoning":{"effort":"none","summary":null},"safety_identifier":null,"service_tier":"default","store":false,"temperature":1.0,"text":{"format":{"type":"text"},"verbosity":null},"tool_choice":"auto","tools":[],"top_logprobs":0,"top_p":1.0,"truncation":"disabled","usage":null,"user":null,"metadata":{}},"sequence_number":1}

event: response.output_item.added
data: {"type":"response.output_item.added","item":{"type":"message","id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","status":"in_progress","content":[],"phase":"final_answer","role":"assistant"},"output_index":0,"sequence_number":2}

event: response.content_part.added
data: {"type":"response.content_part.added","content_index":0,"item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","output_index":0,"part":{"type":"output_text","annotations":[],"logprobs":[],"text":""},"sequence_number":3}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":"Hello","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":4}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":"!","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":5}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" 👋","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":6}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" How","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":7}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" can","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":8}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" I","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":9}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" help","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":10}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" you","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":11}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":" today","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":12}

event: response.output_text.delta
data: {"type":"response.output_text.delta","content_index":0,"delta":"?","item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":13}

event: response.output_text.done
data: {"type":"response.output_text.done","content_index":0,"item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","logprobs":[],"output_index":0,"sequence_number":14,"text":"Hello! 👋 How can I help you today?"}

event: response.content_part.done
data: {"type":"response.content_part.done","content_index":0,"item_id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","output_index":0,"part":{"type":"output_text","annotations":[],"logprobs":[],"text":"Hello! 👋 How can I help you today?"},"sequence_number":15}

event: response.output_item.done
data: {"type":"response.output_item.done","item":{"type":"message","id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","status":"completed","content":[{"type":"output_text","annotations":[],"logprobs":[],"text":"Hello! 👋 How can I help you today?"}],"phase":"final_answer","role":"assistant"},"output_index":0,"sequence_number":16}

event: response.completed
data: {"type":"response.completed","response":{"id":"19460ef2-58da-46c5-9510-9e7b04c47e4a","object":"response","created_at":1793084908,"status":"completed","background":false,"completed_at":1793084909,"content_filters":null,"error":null,"frequency_penalty":0.0,"incomplete_details":null,"instructions":null,"max_output_tokens":32,"max_tool_calls":null,"model":"deepseek-flash","moderation":null,"output":[{"type":"message","id":"7b653eb5-6012-4257-ba1a-4e9dce20bd25","status":"completed","content":[{"type":"output_text","annotations":[],"logprobs":[],"text":"Hello! 👋 How can I help you today?"}],"phase":"final_answer","role":"assistant"}],"parallel_tool_calls":true,"presence_penalty":0.0,"previous_response_id":null,"prompt_cache_key":null,"prompt_cache_retention":null,"reasoning":{"effort":"none","summary":null},"safety_identifier":null,"service_tier":"default","store":false,"temperature":1.0,"text":{"format":{"type":"text"},"verbosity":null},"tool_choice":"auto","tools":[],"top_logprobs":0,"top_p":1.0,"truncation":"disabled","usage":{"input_tokens":7,"input_tokens_details":{"cached_tokens":0},"output_tokens":11,"output_tokens_details":{"reasoning_tokens":0},"total_tokens":18},"user":null,"metadata":{}},"sequence_number":17}
```

Loading...
