---
title: "Chat Completions API"
description: "Creates a model response for the given chat conversation."
source: https://api-docs.deepseek.com/api/create-chat-completion
fetched: 2026-08-27
---

# Chat Completions API

```
POST /chat/completions
```

Creates a model response for the given chat conversation.

## Request

**[application/json]**

**Bodyrequired**

**messagesobject[]required**

**Possible values:** `>= 1`

A list of messages comprising the conversation so far.

- Array [

oneOf

- System message
- User message
- Assistant message
- Tool message

**[System message]**

**content** stringrequired

The contents of the system message.

**role** stringrequired

**Possible values:** [`system`]

The role of the messages author, in this case `system`.

**name** string

An optional name for the participant. Provides the model information to differentiate between participants of the same role.

**[User message]**

**contentobjectrequired**

The contents of the user message. Either a string, or an array of content parts (for image input with the `deepseek-v4-flash-vision-exp` model). See the [Vision guide](../guides/vision.md) for details.

oneOf

- Text content
- Array of content parts

**[Assistant message]**

string

**[Tool message]**

- Array [

oneOf

- Text content part
- Image content part
- File content part

**[Text content]**

**type** stringrequired

**Possible values:** [`text`]

The type of the content part, in this case `text`.

**text** stringrequired

The text content.

**[Array of content parts]**

**type** stringrequired

**Possible values:** [`image_url`]

The type of the content part, in this case `image_url`.

**image\_urlobjectrequired**

**url** stringrequired

Either an `http(s)` URL of the image (max 8192 characters) or a base64-encoded data URL (`data:image/jpeg;base64,...`). Supported formats: JPEG, PNG, GIF, and WebP.

**detail** string

**Possible values:** [`low`, `high`, `original`, `auto`]

Controls how the image is processed. `low` downsamples the image to 512x512 (faster, cheaper). `high`, `original`, and `auto` keep the original image.

**[Text content part]**

**type** stringrequired

**Possible values:** [`file`]

The type of the content part, in this case `file`.

**file\_id** string

The ID of a file uploaded via the [Files API](../guides/files_api.md), of the form `file-api-...`. Mutually exclusive with `file_data`.

**file\_data** string

A base64-encoded data URL of the image (`data:image/jpeg;base64,...`). Mutually exclusive with `file_id`.

**filename** string

An optional filename. Only valid together with `file_data`.

- ]

**role** stringrequired

**Possible values:** [`user`]

The role of the messages author, in this case `user`.

**name** string

An optional name for the participant. Provides the model information to differentiate between participants of the same role.

**[Image content part]**

**content** stringnullablerequired

The contents of the assistant message.

**role** stringrequired

**Possible values:** [`assistant`]

The role of the messages author, in this case `assistant`.

**name** string

An optional name for the participant. Provides the model information to differentiate between participants of the same role.

**prefix** bool

(Beta) Set this to `true` to force the model to start its answer by the content of the supplied prefix in this `assistant` message.
You must set `base_url="https://api.deepseek.com/beta"` to use this feature.

**reasoning\_content** stringnullable

(Beta) Used for the thinking mode in the [Chat Prefix Completion](../guides/chat_prefix_completion.md) feature as the input for the CoT in the last assistant message. When using this feature, the `prefix` parameter must be set to `true`.

**[File content part]**

**role** stringrequired

**Possible values:** [`tool`]

The role of the messages author, in this case `tool`.

**content** Text content (string)required

The contents of the tool message.

**tool\_call\_id** stringrequired

Tool call that this message is responding to.

- ]

**model** stringrequired

**Possible values:** [`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp`]

ID of the model to use.

**thinkingobjectnullable**

Controls the switch between thinking and non-thinking mode.

**type** string

**Possible values:** [`enabled`, `disabled`]

**Default value:** `enabled`

If set to `enabled`, then use thinking mode. If set to `disabled`, then use non-thinking model.

**reasoning\_effort** string

**Possible values:** [`low`, `high`, `max`]

Controls the reasoning effort of the model. The default effort is `high`. For compatibility, `medium` and `xhigh` are mapped to `high`.

**max\_tokens** integernullable

The maximum number of tokens that can be generated in the chat completion.

The total length of input tokens and generated tokens is limited by the model's context length.

For the value range and default value, please refer to the [documentation](../quick_start/pricing.md).

**response\_formatobjectnullable**

An object specifying the format that the model must output.
Setting to { "type": "json\_object" } enables JSON Output, which guarantees the message the model generates is valid JSON.

**Important:** When using JSON Output, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish\_reason="length", which indicates the generation exceeded max\_tokens or the conversation exceeded the max context length.

**type** string

**Possible values:** [`text`, `json_object`]

**Default value:** `text`

Must be one of `text` or `json_object`.

**stopobjectnullable**

Up to 16 sequences where the API will stop generating further tokens.

oneOf

- MOD1
- MOD2

**[MOD1]**

string

**[MOD2]**

- Array [

string

- ]

**stream** booleannullable

If set, partial message deltas will be sent. Tokens will be sent as data-only server-sent events (SSE) as they become available, with the stream terminated by a `data: [DONE]` message.

**stream\_optionsobjectnullable**

Options for streaming response. Only set this when you set `stream: true`.

**include\_usage** boolean

If set to `true`, all chunks in the stream will include a `usage` field, whose value is `null` on every chunk except the last one. If omitted or set to `false`, the `usage` field is absent from all chunks except the last one.

Either way, the last chunk before the `data: [DONE]` message carries the token usage statistics for the entire request in its `usage` field. Note that no separate usage-only chunk is emitted: the statistics ride on the last content chunk, whose `choices` array always contains exactly one element that carries no new content and a non-null `finish_reason`.

**temperature** numbernullable

**Possible values:** `<= 2`

**Default value:** `1`

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or `top_p` but not both.

**top\_p** numbernullable

**Possible values:** `<= 1`

**Default value:** `1`

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or `temperature` but not both.

**toolsobject[]nullable**

A list of tools the model may call. Currently, only functions are supported as a tool.
Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported.

- Array [

**type** stringrequired

**Possible values:** [`function`]

The type of the tool. Currently, only `function` is supported.

**functionobjectrequired**

**description** string

A description of what the function does, used by the model to choose when and how to call the function.

**name** stringrequired

The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.

**parametersobject**

The parameters the functions accepts, described as a JSON Schema object. See the [Tool Calls Guide](../guides/tool_calls.md) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

**property name\*** any

The parameters the functions accepts, described as a JSON Schema object. See the [Tool Calls Guide](../guides/tool_calls.md) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

**strict** boolean

**Default value:** `false`

If set to true, the API will use strict-mode for the tool calls to ensure the output always complies with the function's JSON schema. This is a Beta feature, for more details please refer to [Tool Calls Guide](../guides/tool_calls.md)

- ]

**tool\_choiceobjectnullable**

Controls which (if any) tool is called by the model.

`none` means the model will not call any tool and instead generates a message.

`auto` means the model can pick between generating a message or calling one or more tools.

`required` means the model must call one or more tools.

Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.

`none` is the default when no tools are present. `auto` is the default if tools are present.

oneOf

- ChatCompletionToolChoice
- ChatCompletionNamedToolChoice

**[ChatCompletionToolChoice]**

string

**Possible values:** [`none`, `auto`, `required`]

**[ChatCompletionNamedToolChoice]**

**type** stringrequired

**Possible values:** [`function`]

The type of the tool. Currently, only `function` is supported.

**functionobjectrequired**

**name** stringrequired

The name of the function to call.

**logprobs** booleannullable

Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`.

**top\_logprobs** integernullable

**Possible values:** `<= 20`

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used.

**user\_id** nullable

A custom user\_id. Allowed character set is [a-zA-Z0-9\-\_], with a maximum length of 512. Do not include user privacy information in the user\_id.

- user\_id can be used to distinguish user identities on your side to help us with content safety review.
- user\_id can be used for KVCache isolation for privacy management.
- user\_id can be used for scheduling isolation of users on your business side.
- For more details on the user\_id parameter, please refer to [Rate Limit & Isolation](../quick_start/rate_limit.md)

**frequency\_penalty** deprecated

This parameter is no longer supported. It will not take effect if you pass it to the API.

**presence\_penalty** deprecated

This parameter is no longer supported. It will not take effect if you pass it to the API.

## Responses

- 200 (No streaming)
- 200 (Streaming)

OK, returns a `chat completion object`

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**id** stringrequired

A unique identifier for the chat completion.

**choicesobject[]required**

A list of chat completion choices.

- Array [

**finish\_reason** stringrequired

**Possible values:** [`stop`, `length`, `content_filter`, `tool_calls`, `insufficient_system_resource`]

The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence,
`length` if the maximum number of tokens specified in the request was reached,
`content_filter` if content was omitted due to a flag from our content filters,
`tool_calls` if the model called a tool,
or `insufficient_system_resource` if the request is interrupted due to insufficient resource of the inference system.

**index** integerrequired

The index of the choice in the list of choices.

**messageobjectrequired**

A chat completion message generated by the model.

**content** stringnullablerequired

The contents of the message.

**reasoning\_content** stringnullable

For thinking mode only. The reasoning contents of the assistant message, before the final answer.

**tool\_callsobject[]**

The tool calls generated by the model.

- Array [

**id** stringrequired

The ID of the tool call.

**type** stringrequired

**Possible values:** [`function`]

The type of the tool. Currently, only `function` is supported.

**functionobjectrequired**

The function that the model called.

**name** stringrequired

The name of the function to call.

**arguments** stringrequired

The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

- ]

**role** stringrequired

**Possible values:** [`assistant`]

The role of the author of this message.

**logprobsobjectnullablerequired**

Log probability information for the choice.

**contentobject[]nullablerequired**

A list of message content tokens with log probability information.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

**top\_logprobsobject[]required**

List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

- ]

- ]

**reasoning\_contentobject[]nullable**

A list of message content tokens with log probability information.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

**top\_logprobsobject[]required**

List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

- ]

- ]

- ]

**created** integerrequired

The Unix timestamp (in seconds) of when the chat completion was created.

**model** stringrequired

The model used for the chat completion.

**system\_fingerprint** stringrequired

This fingerprint represents the backend configuration that the model runs with.

**object** stringrequired

**Possible values:** [`chat.completion`]

The object type, which is always `chat.completion`.

**usageobject**

Usage statistics for the completion request.

**completion\_tokens** integerrequired

Number of tokens in the generated completion.

**prompt\_tokens** integerrequired

Number of tokens in the prompt. It equals prompt\_cache\_hit\_tokens + prompt\_cache\_miss\_tokens.

**prompt\_cache\_hit\_tokens** integerrequired

Number of tokens in the prompt that hits the context cache.

**prompt\_cache\_miss\_tokens** integerrequired

Number of tokens in the prompt that misses the context cache.

**total\_tokens** integerrequired

Total number of tokens used in the request (prompt + completion).

**completion\_tokens\_detailsobject**

Breakdown of tokens used in a completion.

**reasoning\_tokens** integer

Tokens generated by the model for reasoning.

**[Example (from schema)]**

```json
{
  "id": "string",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "string",
        "reasoning_content": "string",
        "tool_calls": [
          {
            "id": "string",
            "type": "function",
            "function": {
              "name": "string",
              "arguments": "string"
            }
          }
        ],
        "role": "assistant"
      },
      "logprobs": {
        "content": [
          {
            "token": "string",
            "logprob": 0,
            "bytes": [
              0
            ],
            "top_logprobs": [
              {
                "token": "string",
                "logprob": 0,
                "bytes": [
                  0
                ]
              }
            ]
          }
        ],
        "reasoning_content": [
          {
            "token": "string",
            "logprob": 0,
            "bytes": [
              0
            ],
            "top_logprobs": [
              {
                "token": "string",
                "logprob": 0,
                "bytes": [
                  0
                ]
              }
            ]
          }
        ]
      }
    }
  ],
  "created": 0,
  "model": "string",
  "system_fingerprint": "string",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 0,
    "prompt_tokens": 0,
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 0,
    "total_tokens": 0,
    "completion_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

**[Example]**

```json
{
  "id": "930c60df-bf64-41c9-a88e-3ec75f81e00e",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Hello! How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "created": 1705651092,
  "model": "deepseek-v4-pro",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 10,
    "prompt_tokens": 16,
    "total_tokens": 26
  }
}
```

OK, returns a streamed sequence of `chat completion chunk` objects

**[text/event-stream]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

- Array [

**id** stringrequired

A unique identifier for the chat completion. Each chunk has the same ID.

**choicesobject[]required**

A list of chat completion choices.

- Array [

**deltaobjectrequired**

A chat completion delta generated by streamed model responses.

**content** stringnullable

The contents of the chunk message.

**reasoning\_content** stringnullable

For thinking mode only. The reasoning contents of the assistant message, before the final answer.

**role** string

**Possible values:** [`assistant`]

The role of the author of this message.

**logprobsobjectnullable**

Log probability information for the choice.

**contentobject[]nullablerequired**

A list of message content tokens with log probability information.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

**top\_logprobsobject[]required**

List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

- ]

- ]

**reasoning\_contentobject[]nullable**

A list of message content tokens with log probability information.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

**top\_logprobsobject[]required**

List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned.

- Array [

**token** stringrequired

The token.

**logprob** numberrequired

The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

**bytes** integer[]nullablerequired

A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

- ]

- ]

**finish\_reason** stringnullablerequired

**Possible values:** [`stop`, `length`, `content_filter`, `tool_calls`, `insufficient_system_resource`]

The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence,
`length` if the maximum number of tokens specified in the request was reached,
`content_filter` if content was omitted due to a flag from our content filters,
`tool_calls` if the model called a tool,
or `insufficient_system_resource` if the request is interrupted due to insufficient resource of the inference system.

**index** integerrequired

The index of the choice in the list of choices.

- ]

**created** integerrequired

The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp.

**model** stringrequired

The model to generate the completion.

**system\_fingerprint** stringrequired

This fingerprint represents the backend configuration that the model runs with.

**object** stringrequired

**Possible values:** [`chat.completion.chunk`]

The object type, which is always `chat.completion.chunk`.

- ]

**[Example (from schema)]**

```json
[
  {
    "id": "string",
    "choices": [
      {
        "delta": {
          "content": "string",
          "reasoning_content": "string",
          "role": "assistant"
        },
        "logprobs": {
          "content": [
            {
              "token": "string",
              "logprob": 0,
              "bytes": [
                0
              ],
              "top_logprobs": [
                {
                  "token": "string",
                  "logprob": 0,
                  "bytes": [
                    0
                  ]
                }
              ]
            }
          ],
          "reasoning_content": [
            {
              "token": "string",
              "logprob": 0,
              "bytes": [
                0
              ],
              "top_logprobs": [
                {
                  "token": "string",
                  "logprob": 0,
                  "bytes": [
                    0
                  ]
                }
              ]
            }
          ]
        },
        "finish_reason": "stop",
        "index": 0
      }
    ],
    "created": 0,
    "model": "string",
    "system_fingerprint": "string",
    "object": "chat.completion.chunk"
  }
]
```

**[Example]**

```shell
data: {"id": "1f633d8bfc032625086f14113c411638", "choices": [{"index": 0, "delta": {"content": "", "role": "assistant"}, "finish_reason": null, "logprobs": null}], "created": 1718345013, "model": "deepseek-v4-pro", "system_fingerprint": "fp_a49d71b8a1", "object": "chat.completion.chunk", "usage": null}

data: {"choices": [{"delta": {"content": "Hello", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": "!", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " How", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " can", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " I", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " assist", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " you", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": " today", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": "?", "role": "assistant"}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1"}

data: {"choices": [{"delta": {"content": "", "role": null}, "finish_reason": "stop", "index": 0, "logprobs": null}], "created": 1718345013, "id": "1f633d8bfc032625086f14113c411638", "model": "deepseek-v4-pro", "object": "chat.completion.chunk", "system_fingerprint": "fp_a49d71b8a1", "usage": {"completion_tokens": 9, "prompt_tokens": 17, "total_tokens": 26}}

data: [DONE]
```

Loading...
