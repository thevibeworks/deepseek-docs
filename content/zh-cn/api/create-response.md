---
title: "Responses API"
description: "以 OpenAI Responses API 格式创建模型响应。"
source: https://api-docs.deepseek.com/zh-cn/api/create-response
fetched: 2026-08-23
---

# Responses API

```
POST /responses
```

以 OpenAI Responses API 格式创建模型响应。

该 API 是**无状态**的：服务端不存储响应与会话。多轮对话需要客户端在每次请求的 `input` 中回传完整对话历史。详细说明（含完整的参数兼容性表）请参考 [Responses API 指南](../guides/responses_api.md)。

## Request

**[application/json]**

**Bodyrequired**

**model** stringrequired

**Possible values:** [`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp`]

使用的模型的 ID。

**inputobjectnullable**

模型的输入。既可以传纯字符串（视作一条 `user` 消息），也可以传输入 item 列表。

支持的输入 item 类型为 `message` / `function_call` / `function_call_output` / `custom_tool_call` / `custom_tool_call_output` / `reasoning` / `web_search_call`，其他类型会被忽略。消息角色支持 `user` / `assistant` / `system` / `developer`（`developer` 视同 `user`）。使用 `deepseek-v4-flash-vision-exp` 模型时，`user` / `developer` 消息 item 以及 `function_call_output` / `custom_tool_call_output` item 的 `output` 中支持 `input_image` 内容块；`system` / `assistant` 消息中的图片将返回 `400` 错误。使用其他模型时，`input_image` 内容块会被替换为占位文本。文件输入不支持。

`input` 与 `instructions` 至少传一个。

oneOf

- Text input
- Input item list

**[Text input]**

string

**[Input item list]**

- Array [

**type** string

**Possible values:** [`message`, `function_call`, `function_call_output`, `custom_tool_call`, `custom_tool_call_output`, `reasoning`, `web_search_call`]

输入 item 的类型。对于 `message` item，如果传了 `role`，此字段可省略。`custom_tool_call` / `custom_tool_call_output` item 配合 `apply_patch` custom 工具使用。

**role** string

**Possible values:** [`user`, `assistant`, `system`, `developer`]

用于 `message` item。消息作者的角色。`developer` 视同 `user`。

**contentobject**

用于 `message` item 时为消息内容，可以是纯字符串或 `input_text` / `output_text` / `input_image` 内容块列表。使用 `deepseek-v4-flash-vision-exp` 模型时，`input_image` 内容块携带图片；使用其他模型时会被替换为占位文本。用于 `reasoning` item 时为 `reasoning_text` 内容块列表。

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

**Possible values:** [`input_text`, `output_text`]

内容块的类型。

**text** stringrequired

文本内容。

**[图片内容块]**

**type** stringrequired

**Possible values:** [`input_image`]

内容块的类型，此场景下为 `input_image`。

**image\_url** string

图片来源，可以是图片的 `http(s)` URL（最多 8192 个字符）或 base64 编码的 data URL（`data:image/jpeg;base64,...`）。支持的格式：JPEG、PNG、GIF、WebP。与 `file_id` 互斥：两者都不传返回 `400` 错误（"input\_image must have image\_url or file\_id"），两者都传返回 `400` 错误（"input\_image cannot have both image\_url and file\_id"）。

**detail** string

**Possible values:** [`low`, `high`, `original`, `auto`]

控制图片的处理方式。`low` 将图片缩小到 512x512（更快、更省 token）；`high`、`original` 与 `auto` 保留原图。设置 `file_id` 时该字段被忽略。

**file\_id** string

通过 [Files API](../guides/files_api.md) 上传的图片文件 ID，形如 `file-api-...`。与 `image_url` 互斥；设置 `file_id` 时 `detail` 被忽略。

**[推理文本内容块]**

**type** stringrequired

**Possible values:** [`reasoning_text`]

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

**outputobject**

用于 `function_call_output` / `custom_tool_call_output` item。工具调用的结果，可以是纯字符串或 `input_text` / `input_image` 内容块列表。使用 `deepseek-v4-flash-vision-exp` 模型时，输出中的 `input_image` 内容块会作为真实图片处理；使用其他模型时会被替换为占位文本。

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

**Possible values:** [`input_text`, `output_text`]

内容块的类型。

**text** stringrequired

文本内容。

**[图片内容块]**

**type** stringrequired

**Possible values:** [`input_image`]

内容块的类型，此场景下为 `input_image`。

**image\_url** string

图片来源，可以是图片的 `http(s)` URL（最多 8192 个字符）或 base64 编码的 data URL（`data:image/jpeg;base64,...`）。支持的格式：JPEG、PNG、GIF、WebP。与 `file_id` 互斥：两者都不传返回 `400` 错误（"input\_image must have image\_url or file\_id"），两者都传返回 `400` 错误（"input\_image cannot have both image\_url and file\_id"）。

**detail** string

**Possible values:** [`low`, `high`, `original`, `auto`]

控制图片的处理方式。`low` 将图片缩小到 512x512（更快、更省 token）；`high`、`original` 与 `auto` 保留原图。设置 `file_id` 时该字段被忽略。

**file\_id** string

通过 [Files API](../guides/files_api.md) 上传的图片文件 ID，形如 `file-api-...`。与 `image_url` 互斥；设置 `file_id` 时 `detail` 被忽略。

**[推理文本内容块]**

**type** stringrequired

**Possible values:** [`reasoning_text`]

内容块的类型，此场景下为 `reasoning_text`。

**text** stringrequired

思维链文本内容。

- ]

- ]

**instructions** stringnullable

系统级指令，作为模型上下文中的第一条 system 消息。

**reasoningobjectnullable**

思考模式配置。

**effort** string

**Possible values:** [`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`]

控制思考模式开关与思考强度。`none` 关闭思考模式；`minimal` / `low` 开启思考模式，思考强度为 `low`；`medium` / `high` / `xhigh` 开启思考模式，思考强度为 `high`；`max` 开启思考模式，思考强度为 `max`。不传时使用模型默认的思考行为（默认开启）。

**max\_output\_tokens** integernullable

响应可生成的 token 数上限，包含可见的输出 token 与思维链 token。

**stream** booleannullable

如果设置为 `true`，响应将以语义化的流式 SSE 事件返回。最后一个事件是 `response.completed` / `response.incomplete` / `response.failed`（没有 `data: [DONE]` 消息）。完整事件列表请参考 [Responses API 指南](../guides/responses_api.md#streaming)。

**temperature** numbernullable

**Possible values:** `<= 2`

**Default value:** `1`

采样温度，介于 0 和 2 之间。更高的值（如 0.8）会使输出更随机，而更低的值（如 0.2）会使其更加集中和确定。思考模式下不生效。

**top\_p** numbernullable

**Possible values:** `<= 1`

**Default value:** `1`

作为调节采样温度的替代方案，即核采样。思考模式下不生效。

**textobjectnullable**

文本输出配置。

**formatobject**

输出格式。`{"type": "text"}`（默认）为纯文本输出；`{"type": "json_object"}` 为 JSON 模式；`{"type": "json_schema", "name": ..., "schema": ...}` 为结构化输出，输出符合给定的 JSON Schema。

**type** string

**Possible values:** [`text`, `json_object`, `json_schema`]

**Default value:** `text`

**name** string

schema 的名称。`type` 为 `json_schema` 时必填。

**schema** object

输出必须符合的 JSON Schema。`type` 为 `json_schema` 时必填。

**toolsobject[]nullable**

模型可能会调用的工具的列表。函数名必须非空、不超过 128 个字符、匹配 `^[a-zA-Z0-9_-]+$`，且所有工具的名称必须唯一。除 `function` 外，还支持内置的 `web_search` 工具（服务端执行），其他内置工具类型会被忽略。详情请参考 [Responses API 指南](../guides/responses_api.md)。

- Array [

**type** stringrequired

**Possible values:** [`function`, `web_search`, `web_search_2025_08_26`]

工具的类型。

**name** string

用于 `function` 工具。函数的名称。必须非空、不超过 128 个字符、匹配 `^[a-zA-Z0-9_-]+$`，且所有工具的名称必须唯一。

**description** string

用于 `function` 工具。函数功能的描述，供模型理解何时以及如何调用该函数。

**parametersobject**

function 的输入参数，以 JSON Schema 对象描述。请参阅[Tool Calls 指南](../guides/tool_calls.md)获取示例，并参阅[JSON Schema 参考](https://json-schema.org/understanding-json-schema/)了解有关格式的文档。省略 `parameters` 会定义一个参数列表为空的 function。

**property name\*** any

function 的输入参数，以 JSON Schema 对象描述。请参阅[Tool Calls 指南](../guides/tool_calls.md)获取示例，并参阅[JSON Schema 参考](https://json-schema.org/understanding-json-schema/)了解有关格式的文档。省略 `parameters` 会定义一个参数列表为空的 function。

- ]

**tool\_choiceobjectnullable**

控制模型调用工具的行为。

`none` 意味着模型不会调用任何工具，而是生成一条消息。

`auto`（默认）意味着模型可以选择生成一条消息或调用一个或多个工具。

`required` 意味着模型必须调用一个或多个工具。

通过 `{"type": "function", "name": "my_function"}` 指定特定工具，会强制模型调用该工具。

通过 `{"type": "web_search"}`（或 `{"type": "web_search_2025_08_26"}`）可强制模型执行联网搜索；此时 `tools` 中必须包含 `web_search` 工具，否则返回 `400` 错误。

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

一个介于 0 到 20 之间的整数 N，指定每个输出位置返回输出概率 top N 的 token，且返回这些 token 的对数概率。

**user** stringnullable

自定义终端用户标识，字符集为 [a-zA-Z0-9\-\_]，最大长度为 512。请勿在其中包含用户隐私信息。

- 可用于区分您业务侧的用户身份，以帮助我们进行内容安全审核；也可用于 KVCache 隔离与调度隔离。详情请参考[限速与用户隔离](../quick_start/rate_limit.md)

## Responses

- 200 (No streaming)
- 200 (Streaming)

OK, 返回一个 `response` 对象。

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**id** stringrequired

该响应的唯一标识符。

**object** stringrequired

**Possible values:** [`response`]

object 的类型，其值恒为 `response`。

**created\_at** integerrequired

标志响应创建时间的 Unix 时间戳（以秒为单位）。

**status** stringrequired

**Possible values:** [`in_progress`, `completed`, `incomplete`, `failed`]

响应的状态。

**error** objectnullable

响应失败时的错误对象，包含 `code` 和 `message` 字段。

**incomplete\_detailsobjectnullable**

响应不完整的原因详情。`reason` 字段可能为 `max_output_tokens` 或 `content_filter`。

**reason** string

**Possible values:** [`max_output_tokens`, `content_filter`]

**model** stringrequired

生成该响应的模型。

**outputobject[]required**

模型生成的输出 item 列表。思考模式下，思维链以 `reasoning` item 的形式在 `message` item 之前返回。函数调用以 `function_call` item 返回，服务端联网搜索动作以 `web_search_call` item 返回。

- Array [

**type** string

**Possible values:** [`message`, `reasoning`, `function_call`, `web_search_call`]

输出 item 的类型。

**id** string

输出 item 的唯一 ID。

**status** string

**Possible values:** [`in_progress`, `completed`, `incomplete`]

输出 item 的状态。

**role** string

**Possible values:** [`assistant`]

用于 `message` item。其值恒为 `assistant`。

**contentobject[]**

用于 `message` item 时为 `output_text` 内容块列表。用于 `reasoning` item 时为 `reasoning_text` 内容块列表，以明文承载思维链内容。

- Array [

**type** string

**Possible values:** [`output_text`, `reasoning_text`]

**text** string

- ]

**call\_id** string

用于 `function_call` item。将函数调用结果回传给 API 时使用的标识符。

**name** string

用于 `function_call` item。要调用的函数的名称。

**arguments** string

用于 `function_call` item。模型生成的调用函数的入参，格式为 JSON。请注意，模型并不总是生成有效的 JSON，且可能会虚构出您的函数模式中未定义的参数。在调用函数之前，请在您的代码中验证这些入参是否有效。

**action** object

用于 `web_search_call` item。描述服务端执行的搜索动作（`search` / `open_page` / `find_in_page`）的对象。

- ]

**usageobject**

该响应的 token 用量统计信息。

**input\_tokens** integerrequired

输入 token 数。

**input\_tokens\_detailsobject**

输入 token 的细分信息。

**cached\_tokens** integer

命中上下文缓存的输入 token 数。参考[上下文硬盘缓存](../guides/kv_cache.md)。

**output\_tokens** integerrequired

输出 token 数。

**output\_tokens\_detailsobject**

输出 token 的细分信息。

**reasoning\_tokens** integer

模型生成的思维链 token 数。

**total\_tokens** integerrequired

该请求使用的 token 总数（输入 + 输出）。

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

OK, 返回语义化的流式 SSE 事件序列。每个事件带有表示事件类型的 `event` 字段和递增的 `sequence_number`。最后一个事件是 `response.completed` / `response.incomplete` / `response.failed`（没有 `data: [DONE]` 消息）。完整事件列表请参考 [Responses API 指南](../guides/responses_api.md#streaming)。

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
