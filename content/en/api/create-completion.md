---
title: "FIM Completion API (Beta)"
description: "FIM (Fill In the Middle) Completion API.<br/>User must set `base_url='https://api.deepseek.com/beta'` to use this feature."
source: https://api-docs.deepseek.com/api/create-completion
fetched: 2026-10-31
---

# FIM Completion API (Beta)

[Open Markdown](https://api-docs.deepseek.com/api/create-completion.md "Open Markdown in a new tab")

```
POST /completions
```

FIM (Fill In the Middle) Completion API.
User must set `base_url="https://api.deepseek.com/beta"` to use this feature.

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** `deepseek-flash`, `deepseek-v4-pro`

ID of the model to use. Use `deepseek-flash` or `deepseek-v4-pro`.

**prompt** stringrequired

The prompt to generate completions for.

**echo** booleannullable

**Default value:** `false`

Echo back the prompt in addition to the completion. Cannot be used together with `suffix` or `logprobs`.

**logprobs** integernullable

**Possible values:** `>= 0` and `<= 20`

**Default value:** `null`

Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 20, the API will return a list of the 20 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.

The maximum value for `logprobs` is 20.

**max\_tokens** integernullable

**Possible values:** `>= 0`

The maximum number of tokens that can be generated in the completion.

**stop** string | string[]

nullable

**Default value:** `null`

Up to 16 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.

oneOf

- MOD1
- MOD2

**[MOD1]**

string

**[MOD2]**

**Minimum items:** `1`

**Maximum items:** `16`

- Array [

string

- ]

**stream** booleannullable

**Default value:** `false`

Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).

**stream\_options**

object

nullable

**Default value:** `null`

Options for streaming response. Must be set together with `stream: true`; if `stream` is not set to `true`, the API returns a `400` error.

**include\_usage** boolean

If set to `true`, all chunks in the stream will include a `usage` field, whose value is `null` on every chunk except the last one. If omitted or set to `false`, the `usage` field is absent from all chunks except the last one.

Either way, the last chunk before the `data: [DONE]` message carries the token usage statistics for the entire request in its `usage` field. Note that no separate usage-only chunk is emitted: the statistics ride on the last content chunk, whose `choices` array always contains exactly one element that carries no new content and a non-null `finish_reason`.

**suffix** stringnullable

**Default value:** `null`

The suffix that comes after a completion of inserted text.

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or `top_p` but not both.

**top\_p** numbernullable

**Possible values:** `> 0` and `<= 1`

**Default value:** `1`

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

The value must be greater than 0 and at most 1. We generally recommend altering this or `temperature` but not both.

**frequency\_penalty** nullabledeprecated

This parameter is no longer supported. It will not take effect if you pass it to the API.

**presence\_penalty** nullabledeprecated

This parameter is no longer supported. It will not take effect if you pass it to the API.

## Responses

- 200
- 200 (Streaming)

OK

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

A unique identifier for the completion.

**choices**

object[]

required

The list of completion choices the model generated for the input prompt.

- Array [

**finish\_reason** stringnullablerequired

**Possible values:** `stop`, `length`, `content_filter`, `insufficient_system_resource`, `aborted`

The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence,
`length` if the maximum number of tokens specified in the request was reached,
`content_filter` if content was omitted due to a flag from our content filters,
`insufficient_system_resource` if the request is interrupted due to insufficient resource of the inference system,
or `aborted` if the generation was interrupted.

**index** integerrequired

**logprobs**

object

nullable

required

**text\_offset** integer[]

**token\_logprobs** number[]

**tokens** string[]

**top\_logprobs** object[]

**text** stringrequired

- ]

**created** integerrequired

The Unix timestamp (in seconds) of when the completion was created.

**model** stringrequired

The model used for completion.

**system\_fingerprint** string

This fingerprint represents the backend configuration that the model runs with.

**object** stringrequired

**Possible values:** `text_completion`

The object type, which is always "text\_completion"

**usage**

object

Usage statistics for the completion request.

**completion\_tokens** integerrequired

Number of tokens in the generated completion.

**prompt\_tokens** integerrequired

Number of tokens in the prompt. It equals prompt\_cache\_hit\_tokens + prompt\_cache\_miss\_tokens.

**prompt\_tokens\_details**

object

required

Breakdown of tokens used in the prompt.

**cached\_tokens** integer

Number of tokens in the prompt that hit the context cache. Same as `prompt_cache_hit_tokens`.

**prompt\_cache\_hit\_tokens** integerrequired

Number of tokens in the prompt that hits the context cache.

**prompt\_cache\_miss\_tokens** integerrequired

Number of tokens in the prompt that misses the context cache.

**total\_tokens** integerrequired

Total number of tokens used in the request (prompt + completion).

**completion\_tokens\_details**

object

Breakdown of tokens used in a completion.

**reasoning\_tokens** integer

Tokens generated by the model for reasoning.

**[Example]**

```json
{
  "id": "60f16544-b4f2-4149-9326-79ccc6610d67",
  "choices": [
    {
      "text": "return a + b",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "created": 1793084841,
  "model": "deepseek-flash",
  "system_fingerprint": "e72d3c7f663d3e1383b00b3884cb4501",
  "object": "text_completion",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 4,
    "total_tokens": 16,
    "prompt_tokens_details": {
      "cached_tokens": 0
    },
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 12
  }
}
```

OK, returns completion chunks as server-sent events, followed by `data: [DONE]`.

**[text/event-stream]**

- Schema
- Example

**[Schema]**

**Schema**

Represents a completion response from the API. Note: both the streamed and non-streamed response objects share the same shape (unlike the chat endpoint).

- Array [

**id** stringrequired

A unique identifier for the completion.

**choices**

object[]

required

The list of completion choices the model generated for the input prompt.

- Array [

**finish\_reason** stringnullablerequired

**Possible values:** `stop`, `length`, `content_filter`, `insufficient_system_resource`, `aborted`

The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence,
`length` if the maximum number of tokens specified in the request was reached,
`content_filter` if content was omitted due to a flag from our content filters,
`insufficient_system_resource` if the request is interrupted due to insufficient resource of the inference system,
or `aborted` if the generation was interrupted.

**index** integerrequired

**logprobs**

object

nullable

required

**text\_offset** integer[]

**token\_logprobs** number[]

**tokens** string[]

**top\_logprobs** object[]

**text** stringrequired

- ]

**created** integerrequired

The Unix timestamp (in seconds) of when the completion was created.

**model** stringrequired

The model used for completion.

**system\_fingerprint** string

This fingerprint represents the backend configuration that the model runs with.

**object** stringrequired

**Possible values:** `text_completion`

The object type, which is always "text\_completion"

**usage**

object

Usage statistics for the completion request.

**completion\_tokens** integerrequired

Number of tokens in the generated completion.

**prompt\_tokens** integerrequired

Number of tokens in the prompt. It equals prompt\_cache\_hit\_tokens + prompt\_cache\_miss\_tokens.

**prompt\_tokens\_details**

object

required

Breakdown of tokens used in the prompt.

**cached\_tokens** integer

Number of tokens in the prompt that hit the context cache. Same as `prompt_cache_hit_tokens`.

**prompt\_cache\_hit\_tokens** integerrequired

Number of tokens in the prompt that hits the context cache.

**prompt\_cache\_miss\_tokens** integerrequired

Number of tokens in the prompt that misses the context cache.

**total\_tokens** integerrequired

Total number of tokens used in the request (prompt + completion).

**completion\_tokens\_details**

object

Breakdown of tokens used in a completion.

**reasoning\_tokens** integer

Tokens generated by the model for reasoning.

- ]

**[Example]**

```shell
data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":"","index":0,"logprobs":null,"finish_reason":null}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion"}

data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":"return","index":0,"logprobs":null,"finish_reason":null}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion"}

data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":" a","index":0,"logprobs":null,"finish_reason":null}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion"}

data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":" +","index":0,"logprobs":null,"finish_reason":null}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion"}

data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":" b","index":0,"logprobs":null,"finish_reason":null}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion"}

data: {"id":"79323126-3e6a-4fb3-8d99-71fb50f801fc","choices":[{"text":"","index":0,"logprobs":null,"finish_reason":"stop"}],"created":1793084906,"model":"deepseek-flash","system_fingerprint":"e72d3c7f663d3e1383b00b3884cb4501","object":"text_completion","usage":{"prompt_tokens":12,"completion_tokens":4,"total_tokens":16,"prompt_tokens_details":{"cached_tokens":0},"prompt_cache_hit_tokens":0,"prompt_cache_miss_tokens":12}}

data: [DONE]
```

Loading...
