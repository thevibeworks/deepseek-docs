---
title: "Responses API"
description: "以 OpenAI Responses API 格式创建模型响应。"
source: https://api-docs.deepseek.com/zh-cn/api/create-response
fetched: 2026-10-31
---

# Responses API

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/create-response.md "在新标签页打开 Markdown")

```
POST /responses
```

以 OpenAI Responses API 格式创建模型响应。

该 API 是**无状态**的：服务端不存储响应与会话。多轮对话需要客户端在每次请求的 `input` 中回传完整对话历史。详细说明（含完整的参数兼容性表）请参考 [Responses API 指南](../guides/responses_api.md)。

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** `deepseek-flash`, `deepseek-v4-pro`

使用的模型的 ID。请使用 `deepseek-flash` 或 `deepseek-v4-pro`。

**input** string | object[]

nullable

模型的输入。既可以传纯字符串（视作一条 `user` 消息），也可以传输入 item 列表。

支持的输入 item 类型为 `message` / `function_call` / `function_call_output` / `custom_tool_call` / `custom_tool_call_output` / `reasoning` / `web_search_call`，其他类型会被忽略。消息角色支持 `user` / `assistant` / `system` / `developer`（`developer` 视同 `user`）。使用 `deepseek-flash` 模型时，`user` / `developer` 消息 item 以及 `function_call_output` / `custom_tool_call_output` item 的 `output` 中支持 `input_image` 内容块；`system` / `assistant` 消息中的图片将返回 `400` 错误。文件输入不支持。

`input` 与 `instructions` 至少传一个。

oneOf

- Text input
- Input item list

**[Text input]**

string

**[Input item list]**

输入 item。支持的类型为 `message` / `function_call` / `function_call_output` / `custom_tool_call` / `custom_tool_call_output` / `reasoning` / `web_search_call`，其他类型会被忽略。`reasoning` 和 `function_call` item 会由服务端自动归并到相邻的 assistant 消息中。上一次响应返回的 `web_search_call` item 可以回传，以将其搜索结果还原到上下文中。多轮对话中的回传规则请参考 [Responses API 指南](../guides/responses_api.md#multi-turn-conversation)。

- Array [

**type** string

**Possible values:** `message`, `function_call`, `function_call_output`, `custom_tool_call`, `custom_tool_call_output`, `reasoning`, `web_search_call`

输入 item 的类型。对于 `message` item，如果传了 `role`，此字段可省略。`custom_tool_call` / `custom_tool_call_output` item 配合 `apply_patch` custom 工具使用。`web_search_call` item 用于还原上一次服务端搜索的结果。

**role** string

**Possible values:** `user`, `assistant`, `system`, `developer`

用于 `message` item。消息作者的角色。`developer` 视同 `user`。

**content** string | object[]

用于 `message` item 时为消息内容，可以是纯字符串或 `input_text` / `output_text` / `input_image` 内容块列表。用于 `reasoning` item 时为 `reasoning_text` 内容块列表。

oneOf

- Text content
- Array of content parts

**[Text content]**

string

**[Array of content parts]**

- Array [

oneOf

- 文本内容块
- 图片内容块
- 推理文本内容块

**[文本内容块]**

**type** stringrequired

**Possible values:** `input_text`, `output_text`

内容块的类型。

**text** stringrequired

文本内容。

**[图片内容块]**

图片内容块。会作为真实图片处理。仅允许出现在 `user` / `developer` 消息 item 以及 `function_call_output` / `custom_tool_call_output` item 的 `output` 中；`system` / `assistant` 消息中的图片将返回 `400` 错误（"Image in system message is unsupported" / "Image in assistant message is unsupported"）。

**type** stringrequired

**Possible values:** `input_image`

内容块的类型，此场景下为 `input_image`。

**image\_url** string

图片来源，可以是图片的 `http(s)` URL（最多 8192 个字符）或 base64 编码的 data URL（`data:image/jpeg;base64,...`）。支持的格式：JPEG、PNG、GIF、WebP。与 `file_id` 互斥：两者都不传返回 `400` 错误（"input\_image must have image\_url or file\_id"），两者都传返回 `400` 错误（"input\_image cannot have both image\_url and file\_id"）。

**detail** string

**Possible values:** `low`, `high`, `original`, `auto`

控制图片的处理方式。`low` 将图片缩小到 512x512（更快、更省 token）；`high`、`original` 与 `auto` 保留原图。设置 `file_id` 时该字段被忽略。

**file\_id** string

通过 [Files API](../guides/files_api.md) 上传的图片文件 ID，形如 `file-api-...`。与 `image_url` 互斥；设置 `file_id` 时 `detail` 被忽略。

**[推理文本内容块]**

**type** stringrequired

**Possible values:** `reasoning_text`

内容块的类型，此场景下为 `reasoning_text`。

**text** stringrequired

思维链文本内容。

- ]

**call\_id** string

用于 `function_call` / `function_call_output` item。将函数调用与其结果配对的 ID。必须非空且唯一，且每个 `function_call` 必须有对应的 `function_call_output`。

**name** string

用于 `function_call` item。要调用的函数的名称。

**arguments** string

用于 `function_call` item。调用函数的入参，格式为 JSON。

**output** string | object[]

用于 `function_call_output` / `custom_tool_call_output` item。工具调用的结果，可以是纯字符串或 `input_text` / `input_image` 内容块列表。

oneOf

- Text output
- Array of content parts

**[Text output]**

string

**[Array of content parts]**

- Array [

oneOf

- 文本内容块
- 图片内容块
- 推理文本内容块

**[文本内容块]**

**type** stringrequired

**Possible values:** `input_text`, `output_text`

内容块的类型。

**text** stringrequired

文本内容。

**[图片内容块]**

图片内容块。会作为真实图片处理。仅允许出现在 `user` / `developer` 消息 item 以及 `function_call_output` / `custom_tool_call_output` item 的 `output` 中；`system` / `assistant` 消息中的图片将返回 `400` 错误（"Image in system message is unsupported" / "Image in assistant message is unsupported"）。

**type** stringrequired

**Possible values:** `input_image`

内容块的类型，此场景下为 `input_image`。

**image\_url** string

图片来源，可以是图片的 `http(s)` URL（最多 8192 个字符）或 base64 编码的 data URL（`data:image/jpeg;base64,...`）。支持的格式：JPEG、PNG、GIF、WebP。与 `file_id` 互斥：两者都不传返回 `400` 错误（"input\_image must have image\_url or file\_id"），两者都传返回 `400` 错误（"input\_image cannot have both image\_url and file\_id"）。

**detail** string

**Possible values:** `low`, `high`, `original`, `auto`

控制图片的处理方式。`low` 将图片缩小到 512x512（更快、更省 token）；`high`、`original` 与 `auto` 保留原图。设置 `file_id` 时该字段被忽略。

**file\_id** string

通过 [Files API](../guides/files_api.md) 上传的图片文件 ID，形如 `file-api-...`。与 `image_url` 互斥；设置 `file_id` 时 `detail` 被忽略。

**[推理文本内容块]**

**type** stringrequired

**Possible values:** `reasoning_text`

内容块的类型，此场景下为 `reasoning_text`。

**text** stringrequired

思维链文本内容。

- ]

- ]

**instructions** stringnullable

系统级指令，作为模型上下文中的第一条 system 消息。

**reasoning**

object

nullable

思考模式配置。

**effort** string

**Possible values:** `none`, `low`, `high`, `max`

控制思考模式开关与思考强度。`none` 关闭思考模式；`low` / `high` / `max` 开启思考模式。不传时使用模型默认的思考行为（默认开启）。出于兼容考虑，`minimal` 映射为 `low`，`medium` / `xhigh` 映射为 `high`。

**max\_output\_tokens** integernullable

响应可生成的 token 数上限，包含可见的输出 token 与思维链 token。

**stream** booleannullable

**Default value:** `false`

如果设置为 `true`，响应将以语义化的流式 SSE 事件返回。最后一个事件是 `response.completed` / `response.incomplete` / `response.failed`（没有 `data: [DONE]` 消息）。完整事件列表请参考 [Responses API 指南](../guides/responses_api.md#streaming)。

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

采样温度，介于 0 和 2 之间。更高的值（如 0.8）会使输出更随机，而更低的值（如 0.2）会使其更加集中和确定。思考模式下不生效。

**top\_p** numbernullable

**Possible values:** `>= 0` and `<= 1`

用于调节输出的随机性，可替代 `temperature`。实际生效值取决于模型和模式：

- `deepseek-flash`：思考模式下默认值为 1.0，低于 0.95 的取值会按 0.95 处理；非思考模式下恒为 1.0，传入的值会被忽略。
- `deepseek-v4-pro`：思考模式下，启用工具调用时恒为 0.95，否则恒为 1.0，传入的值会被忽略。即使提供了 `tools`，将 `tool_choice` 设为 `none` 也会关闭工具调用。非思考模式下使用传入的值，默认值为 1.0。

**text**

object

nullable

文本输出配置。

**format**

object

输出格式。`{"type": "text"}`（默认）为纯文本输出；`{"type": "json_object"}` 为 JSON 模式；`{"type": "json_schema", "name": ..., "schema": ...}` 为结构化输出，输出符合给定的 JSON Schema。

省略 `text`、将 `text` 设为 `null`，或省略 `format` 时，使用纯文本输出。提供 `format` 对象时，`type` 必填。

**type** stringrequired

**Possible values:** `text`, `json_object`, `json_schema`

**name** string

schema 的名称。`type` 为 `json_schema` 时必填。

**schema** object

输出必须符合的 JSON Schema。`type` 为 `json_schema` 时必填。

**tools**

object[]

nullable

模型可能会调用的工具的列表。函数名必须非空、不超过 128 个字符、匹配 `^[a-zA-Z0-9_-]+$`，且所有工具的名称必须唯一。支持 `function` 工具；`web_search` 在 `deepseek-v4-pro` 下支持，其余内置工具类型会被忽略。详情请参考 [Responses API 指南](../guides/responses_api.md)。

模型可能会调用的工具。`function` 定义一个函数工具——注意在 Responses API 格式中，`name` / `parameters` 等函数字段位于工具对象的顶层。`custom` 定义 custom 工具，仅支持 `{"type": "custom", "name": "apply_patch"}`，其他名称会返回 `400` 错误。`web_search` 启用服务端网页搜索，在 `deepseek-v4-pro` 下支持。

- Array [

**type** stringrequired

**Possible values:** `function`, `custom`, `web_search`

工具的类型：`function`、`custom`（仅 `apply_patch`）或 `web_search`（仅 `deepseek-v4-pro`）。

**name** string

用于 `function` / `custom` 工具。工具的名称。对于函数工具，必须非空、不超过 128 个字符、匹配 `^[a-zA-Z0-9_-]+$`，且所有工具的名称必须唯一。对于 custom 工具，必须为 `apply_patch`。

**description** string

用于 `function` 工具。函数功能的描述，供模型理解何时以及如何调用该函数。

**parameters**

object

function 的输入参数，以 JSON Schema 对象描述。请参阅[Tool Calls 指南](../guides/tool_calls.md)获取示例，并参阅[JSON Schema 参考](https://json-schema.org/understanding-json-schema/)了解有关格式的文档。省略 `parameters` 会定义一个参数列表为空的 function。

**property name\*** anynullable

- ]

**tool\_choice** string | object

nullable

控制模型调用工具的行为。

`none` 意味着模型不会调用任何工具，而是生成一条消息。

`auto`（默认）意味着模型可以选择生成一条消息或调用一个或多个工具。

`required` 意味着模型必须调用一个或多个工具。

通过 `{"type": "function", "name": "my_function"}` 指定特定工具，会强制模型调用该工具。

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

一个介于 0 到 20 之间的整数 N，指定每个输出位置返回输出概率 top N 的 token，且返回这些 token 的对数概率。

**user** stringnullable

自定义终端用户标识。建议仅使用英文字母、数字、下划线（`_`）和连字符（`-`）。UTF-8 编码后不得超过 512 字节。请勿在其中包含用户隐私信息。

- 可用于区分您业务侧的用户身份，以帮助我们进行内容安全审核；也可用于 KVCache 隔离与调度隔离。详情请参考[限速与用户隔离](../quick_start/rate_limit.md)

## Responses

- 200 (No streaming)
- 200 (Streaming)

OK, 返回一个 `response` 对象。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

该响应的唯一标识符。

**object** stringrequired

**Possible values:** `response`

object 的类型，其值恒为 `response`。

**created\_at** integerrequired

标志响应创建时间的 Unix 时间戳（以秒为单位）。

**status** stringrequired

**Possible values:** `in_progress`, `completed`, `incomplete`, `failed`

响应的状态。

**error** objectnullable

响应失败时的错误对象，包含 `code` 和 `message` 字段。

**incomplete\_details**

object

nullable

响应不完整的原因详情。`reason` 字段可能为 `max_output_tokens` 或 `content_filter`。

**reason** string

**Possible values:** `max_output_tokens`, `content_filter`

**model** stringrequired

生成该响应的模型。

**output**

object[]

required

模型生成的输出 item 列表。思考模式下，思维链以 `reasoning` item 的形式在 `message` item 之前返回。函数调用以 `function_call` item 返回。

模型生成的输出 item。`message` item 承载模型回复文本，`reasoning` item 承载思维链，`function_call` item 表示函数调用，`custom_tool_call` item 表示 custom 工具调用（如 `apply_patch`），`web_search_call` item 表示服务端网页搜索（仅 `deepseek-v4-pro`），`tool_search_call` item 表示工具搜索。

- Array [

**type** string

**Possible values:** `message`, `reasoning`, `function_call`, `custom_tool_call`, `web_search_call`, `tool_search_call`

输出 item 的类型：`message` / `reasoning` / `function_call` / `custom_tool_call` / `web_search_call` / `tool_search_call`。

**id** string

输出 item 的唯一 ID。

**status** string

**Possible values:** `in_progress`, `completed`, `incomplete`

输出 item 的状态。

**role** string

**Possible values:** `assistant`

用于 `message` item。其值恒为 `assistant`。

**content**

object[]

用于 `message` item 时为 `output_text` 内容块列表。用于 `reasoning` item 时为 `reasoning_text` 内容块列表，以明文承载思维链内容。

- Array [

**type** string

**Possible values:** `output_text`, `reasoning_text`

**text** string

- ]

**call\_id** string

用于 `function_call` / `custom_tool_call` / `tool_search_call` item。将工具结果回传给 API 时使用的标识符。

**name** string

用于 `function_call` / `custom_tool_call` item。要调用的函数或 custom 工具的名称。

**arguments** string

用于 `function_call` item。模型生成的调用函数的入参，格式为 JSON。请注意，模型并不总是生成有效的 JSON，且可能会虚构出您的函数模式中未定义的参数。在调用函数之前，请在您的代码中验证这些入参是否有效。

- ]

**usage**

object

nullable

该响应的 token 和服务端工具用量统计信息。流式响应的初始事件中为 null，请读取最终响应的 usage。

**input\_tokens** integerrequired

输入 token 数。

**input\_tokens\_details**

object

输入 token 的细分信息。

**cached\_tokens** integer

命中上下文缓存的输入 token 数。参考[上下文硬盘缓存](../guides/kv_cache.md)。

**output\_tokens** integerrequired

输出 token 数。

**output\_tokens\_details**

object

输出 token 的细分信息。

**reasoning\_tokens** integer

模型生成的思维链 token 数。

**total\_tokens** integerrequired

该请求使用的 token 总数（输入 + 输出）。

**server\_tool\_use**

object

成功的服务端网页搜索和抓取次数，与 token 用量分别统计。仅在 tool\_search 或 tool\_fetch 大于零时返回，否则省略整个字段。返回时两个子字段均存在。流式响应中，请从终止事件 response.completed、response.incomplete 或 response.failed 的 response.usage 读取。这些计数是累计值，不是增量。详见[服务端工具用量](../guides/responses_api.md#server-tool-usage)。

**tool\_search** integerrequired

**Possible values:** `>= 0`

成功的网页搜索查询次数。一次搜索含多个查询时可能累计多次；失败或结果为空的查询不计入。此字段可作为计费依据。

**tool\_fetch** integerrequired

**Possible values:** `>= 0`

通过 open\_page 或 find\_in\_page 成功抓取网页的次数。失败的尝试不计入。此字段可作为计费依据。

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

OK, 返回语义化的流式 SSE 事件序列。每个事件带有表示事件类型的 `event` 字段和递增的 `sequence_number`。最后一个事件是 `response.completed` / `response.incomplete` / `response.failed`（没有 `data: [DONE]` 消息）。完整事件列表请参考 [Responses API 指南](../guides/responses_api.md#streaming)。

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
