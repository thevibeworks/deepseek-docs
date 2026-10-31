---
title: "FIM 补全 API（Beta）"
description: "FIM (Fill In the Middle) 补全 API。<br/>用户需要设置 `base_url='https://api.deepseek.com/beta'` 来使用此功能。"
source: https://api-docs.deepseek.com/zh-cn/api/create-completion
fetched: 2026-10-31
---

# FIM 补全 API（Beta）

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/create-completion.md "在新标签页打开 Markdown")

```
POST /completions
```

FIM (Fill In the Middle) 补全 API。
用户需要设置 `base_url="https://api.deepseek.com/beta"` 来使用此功能。

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** `deepseek-flash`, `deepseek-v4-pro`

模型的 ID。请使用 `deepseek-flash` 或 `deepseek-v4-pro`。

**prompt** stringrequired

用于生成完成内容的提示

**echo** booleannullable

**Default value:** `false`

在输出中，把 prompt 的内容也输出出来。不能与 `suffix` 或 `logprobs` 一起使用。

**logprobs** integernullable

**Possible values:** `>= 0` and `<= 20`

**Default value:** `null`

制定输出中包含 logprobs 最可能输出 token 的对数概率，包含采样的 token。例如，如果 logprobs 是 20，API 将返回一个包含 20 个最可能的 token 的列表。API 将始终返回采样 token 的对数概率，因此响应中可能会有最多 logprobs+1 个元素。

logprobs 的最大值是 20。

**max\_tokens** integernullable

**Possible values:** `>= 0`

最大生成 token 数量。

**stop** string | string[]

nullable

**Default value:** `null`

一个 string 或最多包含 16 个 string 的 list，在遇到这些词时，API 将停止生成更多的 token。

oneOf

- MOD1
- MOD2

**[MOD1]**

string

**[MOD2]**

**最少元素数：** `1`

**最多元素数：** `16`

- Array [

string

- ]

**stream** booleannullable

**Default value:** `false`

如果设置为 `true`，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 `data: [DONE]` 结尾。

**stream\_options**

object

nullable

**Default value:** `null`

流式输出相关选项。必须与 `stream: true` 一起使用；如果 `stream` 未设置为 `true`，API 会返回 `400` 错误。

**include\_usage** boolean

如果设置为 `true`，流式返回的所有块都会包含 `usage` 字段，其中除最后一个块外，该字段的值均为 `null`。如果不设置或设置为 `false`，则除最后一个块外，其余块都不含 `usage` 字段。

无论是否设置，`data: [DONE]` 之前的最后一个块都会在其 `usage` 字段中给出整个请求的 token 使用统计信息。请注意，这里不会单独下发一个只含 usage 的块：统计信息附加在最后一个内容块上，该块的 `choices` 数组始终只包含一个元素，其中不含新增内容且 `finish_reason` 非 null。

**suffix** stringnullable

**Default value:** `null`

制定被补全内容的后缀。

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

采样温度，介于 0 和 2 之间。更高的值，如 0.8，会使输出更随机，而更低的值，如 0.2，会使其更加集中和确定。 我们通常建议可以更改这个值或者更改 `top_p`，但不建议同时对两者进行修改。

**top\_p** numbernullable

**Possible values:** `> 0` and `<= 1`

**Default value:** `1`

作为调节采样温度的替代方案，模型会考虑前 `top_p` 概率的 token 的结果。所以 0.1 就意味着只有包括在最高 10% 概率中的 token 会被考虑。 取值必须大于 0 且不超过 1。我们通常建议修改这个值或者更改 `temperature`，但不建议同时对两者进行修改。

**frequency\_penalty** nullabledeprecated

该参数已不再支持。传入该参数将不会产生任何效果。

**presence\_penalty** nullabledeprecated

该参数已不再支持。传入该参数将不会产生任何效果。

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

补全响应的 ID。

**choices**

object[]

required

模型生成的补全内容的选择列表。

- Array [

**finish\_reason** stringnullablerequired

**Possible values:** `stop`, `length`, `content_filter`, `insufficient_system_resource`, `aborted`

模型停止生成 token 的原因。

`stop`：模型自然停止生成，或遇到 `stop` 序列中列出的字符串。

`length` ：输出长度达到了模型上下文长度限制，或达到了 `max_tokens` 的限制。

`content_filter`：输出内容因触发过滤策略而被过滤。

`insufficient_system_resource`: 由于后端推理资源受限，请求被打断。

`aborted`：生成过程被中断。

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

标志补全请求开始时间的 Unix 时间戳（以秒为单位）。

**model** stringrequired

补全请求所用的模型。

**system\_fingerprint** string

模型运行时的后端配置的指纹。

**object** stringrequired

**Possible values:** `text_completion`

object 的类型，一定为"text\_completion"

**usage**

object

该对话补全请求的用量信息。

**completion\_tokens** integerrequired

模型 completion 产生的 token 数。

**prompt\_tokens** integerrequired

用户 prompt 所包含的 token 数。该值等于 `prompt_cache_hit_tokens + prompt_cache_miss_tokens`

**prompt\_tokens\_details**

object

required

prompt tokens 的详细信息。

**cached\_tokens** integer

用户 prompt 中，命中上下文缓存的 token 数。与 `prompt_cache_hit_tokens` 相同。

**prompt\_cache\_hit\_tokens** integerrequired

用户 prompt 中，命中上下文缓存的 token 数。

**prompt\_cache\_miss\_tokens** integerrequired

用户 prompt 中，未命中上下文缓存的 token 数。

**total\_tokens** integerrequired

该请求中，所有 token 的数量（prompt + completion）。

**completion\_tokens\_details**

object

completion tokens 的详细信息。

**reasoning\_tokens** integer

推理模型所产生的思维链 token 数量

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

OK, 以 SSE 事件逐步返回补全内容，最后发送 `data: [DONE]`。

**[text/event-stream]**

- Schema
- Example

**[Schema]**

**Schema**

补全 API 的响应。注意：流式和非流式响应对象具有相同的结构（与对话补全不同）。

- Array [

**id** stringrequired

补全响应的 ID。

**choices**

object[]

required

模型生成的补全内容的选择列表。

- Array [

**finish\_reason** stringnullablerequired

**Possible values:** `stop`, `length`, `content_filter`, `insufficient_system_resource`, `aborted`

模型停止生成 token 的原因。

`stop`：模型自然停止生成，或遇到 `stop` 序列中列出的字符串。

`length` ：输出长度达到了模型上下文长度限制，或达到了 `max_tokens` 的限制。

`content_filter`：输出内容因触发过滤策略而被过滤。

`insufficient_system_resource`: 由于后端推理资源受限，请求被打断。

`aborted`：生成过程被中断。

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

标志补全请求开始时间的 Unix 时间戳（以秒为单位）。

**model** stringrequired

补全请求所用的模型。

**system\_fingerprint** string

模型运行时的后端配置的指纹。

**object** stringrequired

**Possible values:** `text_completion`

object 的类型，一定为"text\_completion"

**usage**

object

该对话补全请求的用量信息。

**completion\_tokens** integerrequired

模型 completion 产生的 token 数。

**prompt\_tokens** integerrequired

用户 prompt 所包含的 token 数。该值等于 `prompt_cache_hit_tokens + prompt_cache_miss_tokens`

**prompt\_tokens\_details**

object

required

prompt tokens 的详细信息。

**cached\_tokens** integer

用户 prompt 中，命中上下文缓存的 token 数。与 `prompt_cache_hit_tokens` 相同。

**prompt\_cache\_hit\_tokens** integerrequired

用户 prompt 中，命中上下文缓存的 token 数。

**prompt\_cache\_miss\_tokens** integerrequired

用户 prompt 中，未命中上下文缓存的 token 数。

**total\_tokens** integerrequired

该请求中，所有 token 的数量（prompt + completion）。

**completion\_tokens\_details**

object

completion tokens 的详细信息。

**reasoning\_tokens** integer

推理模型所产生的思维链 token 数量

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
