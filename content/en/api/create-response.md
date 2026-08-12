---
title: "Responses API"
description: "Creates a model response in the OpenAI Responses API format."
source: https://api-docs.deepseek.com/api/create-response
fetched: 2026-08-12
---

# Responses API

```
POST /responses
```

Creates a model response in the OpenAI Responses API format.

The API is **stateless**: responses and conversations are not stored on the server. For multi-turn conversations, the client needs to send the full conversation history in `input` on each request. Please refer to the [Responses API Guide](../guides/responses_api.md) for details, including the full parameter compatibility tables.

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** [`deepseek-v4-flash`, `deepseek-v4-pro`]

ID of the model to use.

**inputobjectnullable**

The input to the model. Either a plain string (treated as a single `user` message), or a list of input items.

Supported input item types are `message` / `function_call` / `function_call_output` / `reasoning` / `web_search_call`; other types are ignored. Message roles can be `user` / `assistant` / `system` / `developer` (`developer` is treated as `system`). Image and file inputs are not supported (`input_image` parts do not cause an error, but are replaced with a placeholder text).

At least one of `input` and `instructions` is required.

oneOf

- Text input
- Input item list

**[Text input]**

string

**[Input item list]**

- Array [

**type** string

**Possible values:** [`message`, `function_call`, `function_call_output`, `reasoning`, `web_search_call`]

The type of the input item. For `message` items, this field can be omitted if `role` is present.

**role** string

**Possible values:** [`user`, `assistant`, `system`, `developer`]

For `message` items. The role of the message author. `developer` is treated as `system`.

**content**

For `message` items, the message content, either a plain string or a list of `input_text` / `output_text` content parts. For `reasoning` items, a list of `reasoning_text` content parts.

**call\_id** string

For `function_call` / `function_call_output` items. The ID pairing a function call with its output. Must be non-empty and unique, and every `function_call` must have a matching `function_call_output`.

**name** string

For `function_call` items. The name of the function to call.

**arguments** string

For `function_call` items. The arguments to call the function with, in JSON format.

**output** string

For `function_call_output` items. The output of the function call.

- ]

**instructions** stringnullable

A system-level instruction, inserted as the first system message of the model's context.

**reasoningobjectnullable**

Configuration of the thinking mode.

**effort** string

**Possible values:** [`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`]

Controls the thinking mode toggle and the thinking effort. `none` disables thinking mode; `minimal` / `low` enable thinking mode with effort `low`; `medium` / `high` / `xhigh` enable thinking mode with effort `high`; `max` enables thinking mode with effort `max`. If not set, the model's default thinking behavior is used (enabled by default).

**max\_output\_tokens** integernullable

An upper bound for the number of tokens that can be generated in the response, including both the visible output tokens and the reasoning tokens.

**stream** booleannullable

If set to `true`, the response is streamed as semantic server-sent events. The final event is `response.completed` / `response.incomplete` / `response.failed` (there is no `data: [DONE]` message). Please refer to the [Responses API Guide](../guides/responses_api.md#streaming) for the full event list.

**temperature** numbernullable

**Possible values:** `<= 2`

**Default value:** `1`

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Has no effect in thinking mode.

**top\_p** numbernullable

**Possible values:** `<= 1`

**Default value:** `1`

An alternative to sampling with temperature, called nucleus sampling. Has no effect in thinking mode.

**textobjectnullable**

Configuration of the text output.

**formatobject**

The output format. `{"type": "text"}` (default) for plain text; `{"type": "json_object"}` for JSON mode; `{"type": "json_schema", "name": ..., "schema": ...}` for structured output conforming to the given JSON Schema.

**type** string

**Possible values:** [`text`, `json_object`, `json_schema`]

**Default value:** `text`

**name** string

The name of the schema. Required when `type` is `json_schema`.

**schema** object

The JSON Schema that the output must conform to. Required when `type` is `json_schema`.

**toolsobject[]nullable**

A list of tools the model may call. Function names must be non-empty, at most 128 characters, match `^[a-zA-Z0-9_-]+$`, and be unique across all tools. Besides `function`, the built-in `web_search` tool is supported and executed on the server side. Other built-in tool types are ignored. Please refer to the [Responses API Guide](../guides/responses_api.md) for details.

- Array [

**type** stringrequired

**Possible values:** [`function`, `web_search`, `web_search_2025_08_26`]

The type of the tool.

**name** string

For `function` tools. The name of the function. Must be non-empty, at most 128 characters, match `^[a-zA-Z0-9_-]+$`, and be unique across all tools.

**description** string

For `function` tools. A description of what the function does, used by the model to choose when and how to call the function.

**parametersobject**

The parameters the functions accepts, described as a JSON Schema object. See the [Tool Calls Guide](../guides/tool_calls.md) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

**property name\*** any

The parameters the functions accepts, described as a JSON Schema object. See the [Tool Calls Guide](../guides/tool_calls.md) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

- ]

**tool\_choiceobjectnullable**

Controls which (if any) tool is called by the model.

`none` means the model will not call any tool and instead generates a message.

`auto` (default) means the model can pick between generating a message or calling one or more tools.

`required` means the model must call one or more tools.

Specifying a particular tool via `{"type": "function", "name": "my_function"}` forces the model to call that tool.

Specifying `{"type": "web_search"}` (or `{"type": "web_search_2025_08_26"}`) forces the model to perform a web search; the `web_search` tool must be present in `tools`, otherwise a `400` error is returned.

oneOf

- Tool choice mode
- Named tool choice

**[Tool choice mode]**

string

**Possible values:** [`none`, `auto`, `required`]

**[Named tool choice]**

**type** stringrequired

**Possible values:** [`function`, `web_search`, `web_search_2025_08_26`]

**name** string

The name of the function to call. Required when `type` is `function`.

**top\_logprobs** integernullable

**Possible values:** `<= 20`

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

**user** stringnullable

A custom end-user identifier, with allowed character set [a-zA-Z0-9\-\_] and a maximum length of 512. Do not include user privacy information.

- It can be used to distinguish user identities on your side to help us with content safety review, for KVCache isolation, and for scheduling isolation. For more details, please refer to [Rate Limit & Isolation](../quick_start/rate_limit.md)

## Responses

- 200 (No streaming)
- 200 (Streaming)

OK, returns a `response` object

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**id** stringrequired

A unique identifier for the response.

**object** stringrequired

**Possible values:** [`response`]

The object type, which is always `response`.

**created\_at** integerrequired

The Unix timestamp (in seconds) of when the response was created.

**status** stringrequired

**Possible values:** [`in_progress`, `completed`, `incomplete`, `failed`]

The status of the response.

**error** objectnullable

The error object when the response failed, with `code` and `message` fields.

**incomplete\_detailsobjectnullable**

The details about why the response is incomplete. The `reason` field can be `max_output_tokens` or `content_filter`.

**reason** string

**Possible values:** [`max_output_tokens`, `content_filter`]

**model** stringrequired

The model used for the response.

**outputobject[]required**

The list of output items generated by the model. In thinking mode, the chain-of-thought is returned as a `reasoning` item before the `message` item. Function calls are returned as `function_call` items, and server-side web search actions as `web_search_call` items.

- Array [

**type** string

**Possible values:** [`message`, `reasoning`, `function_call`, `web_search_call`]

The type of the output item.

**id** string

The unique ID of the output item.

**status** string

**Possible values:** [`in_progress`, `completed`, `incomplete`]

The status of the output item.

**role** string

**Possible values:** [`assistant`]

For `message` items. Always `assistant`.

**contentobject[]**

For `message` items, a list of `output_text` content parts. For `reasoning` items, a list of `reasoning_text` content parts carrying the chain-of-thought in plain text.

- Array [

**type** string

**Possible values:** [`output_text`, `reasoning_text`]

**text** string

- ]

**call\_id** string

For `function_call` items. An identifier used when passing the function output back to the API.

**name** string

For `function_call` items. The name of the function to call.

**arguments** string

For `function_call` items. The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

**action** object

For `web_search_call` items. An object describing the search action (`search` / `open_page` / `find_in_page`) executed on the server side.

- ]

**usageobject**

Token usage statistics for the response.

**input\_tokens** integerrequired

Number of input tokens.

**input\_tokens\_detailsobject**

Breakdown of the input tokens.

**cached\_tokens** integer

Number of input tokens that hit the context cache. See [Context Caching](../guides/kv_cache.md).

**output\_tokens** integerrequired

Number of output tokens.

**output\_tokens\_detailsobject**

Breakdown of the output tokens.

**reasoning\_tokens** integer

Number of reasoning (chain-of-thought) tokens generated by the model.

**total\_tokens** integerrequired

Total number of tokens used in the request (input + output).

**[Example (from schema)]**

```json
{
  "id": "string",
  "object": "response",
  "created_at": 0,
  "status": "in_progress",
  "error": {},
  "incomplete_details": {
    "reason": "max_output_tokens"
  },
  "model": "string",
  "output": [
    {
      "type": "message",
      "id": "string",
      "status": "in_progress",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "string"
        }
      ],
      "call_id": "string",
      "name": "string",
      "arguments": "string",
      "action": {}
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}
```

**[Example]**

```json
{
  "id": "24778070-1c36-4ae0-a4bd-870afc7fc13e",
  "object": "response",
  "created_at": 1753000000,
  "status": "completed",
  "model": "deepseek-v4-flash",
  "output": [
    {
      "type": "reasoning",
      "id": "rs_1",
      "status": "completed",
      "content": [
        {
          "type": "reasoning_text",
          "text": "The user greets me. I should reply politely."
        }
      ],
      "summary": []
    },
    {
      "type": "message",
      "id": "msg_1",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Hello! How can I help you today?",
          "annotations": []
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 22,
    "input_tokens_details": { "cached_tokens": 0 },
    "output_tokens": 29,
    "output_tokens_details": { "reasoning_tokens": 27 },
    "total_tokens": 51
  },
  "store": false,
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "error": null,
  "incomplete_details": null
}
```

OK, returns a streamed sequence of semantic server-sent events. Each event has an `event` field for the event type and an incrementing `sequence_number`. The final event is `response.completed` / `response.incomplete` / `response.failed` (there is no `data: [DONE]` message). Please refer to the [Responses API Guide](../guides/responses_api.md#streaming) for the full event list.

**[text/event-stream]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

- Array [

object

- ]

**[Example (from schema)]**

```json
[
  {}
]
```

**[Example]**

```shell
event: response.created
data: {"type": "response.created", "sequence_number": 0, "response": {"id": "...", "object": "response", "status": "in_progress", ...}}

event: response.output_item.added
data: {"type": "response.output_item.added", "sequence_number": 2, "output_index": 0, "item": {"type": "reasoning", ...}}

event: response.reasoning_text.delta
data: {"type": "response.reasoning_text.delta", "sequence_number": 4, "item_id": "rs_1", "output_index": 0, "content_index": 0, "delta": "The user"}

event: response.output_item.added
data: {"type": "response.output_item.added", "sequence_number": 9, "output_index": 1, "item": {"type": "message", "role": "assistant", ...}}

event: response.output_text.delta
data: {"type": "response.output_text.delta", "sequence_number": 11, "item_id": "msg_1", "output_index": 1, "content_index": 0, "delta": "Hello"}

event: response.completed
data: {"type": "response.completed", "sequence_number": 20, "response": {"id": "...", "object": "response", "status": "completed", "usage": {...}, ...}}
```

Loading...
