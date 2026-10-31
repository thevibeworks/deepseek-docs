---
title: "Messages API"
description: "以 Anthropic Messages API 格式创建模型响应。"
source: https://api-docs.deepseek.com/zh-cn/api/create-message
fetched: 2026-10-31
---

# Messages API

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/create-message.md "在新标签页打开 Markdown")

```
POST /anthropic/v1/messages
```

以 Anthropic Messages API 格式创建模型响应。

每次请求都需要在 `messages` 中提供对话历史。Anthropic SDK 的 `base_url` 使用 `https://api.deepseek.com/anthropic`，SDK 会追加 `/v1/messages`。直接发送 HTTP 请求时，也可以使用兼容路径 `/anthropic/messages`。

支持通过 `x-api-key` 或 `Authorization: Bearer` 验证身份。同时提供两者时，优先使用 `Authorization`。模型映射、工具结果回传与兼容性细节请参考 [Anthropic API 指南](../guides/anthropic_api.md)。

兼容字段 `container`、`mcp_servers`、`service_tier` 和 `top_k` 会被忽略。

## Request

**Header Parameters**

**anthropic-version** string

Anthropic SDK 会自动发送此请求头，服务端目前会忽略它。

**Example:** 2023-06-01

**anthropic-beta** string

通过 `source.type` 为 `file` 的图片引用已上传文件时，需包含 `files-api-2025-04-14`。此接口的其他请求无需提供。详见 [Files API 指南](../guides/files_api.md#anthropic-compatible-files-api)。

**Example:** files-api-2025-04-14

**[application/json]**

**Bodyrequired**

**model** stringrequired

要使用的模型 ID，可使用 `deepseek-flash` 或 `deepseek-v4-pro`。也接受 Claude 模型名称别名：`claude-opus*` 映射为 `deepseek-v4-pro`，其它 `claude*` 名称映射为 `deepseek-flash`。详见 [Anthropic API 指南](../guides/anthropic_api.md)。

**messages**

object[]

required

**最少元素数：** `1`

对话历史。至少包含 1 条消息。该 API 是无状态的，每次请求都需要传入本轮所需的历史消息。系统提示词使用顶层 `system` 字段。工具调用后继续对话时，请回传完整的 assistant 内容（包括思考块和工具调用块），随后传入对应的工具结果。服务端可能根据工具调用 ID 恢复遗漏的思考内容，需要恢复但无法恢复时返回 `400`。为保证回传可靠性，请保留完整内容。

- Array [

oneOf

- 用户消息
- 助手消息

**[用户消息]**

**role** stringrequired

**Possible values:** `user`

**content** string | object[]

required

oneOf

- 文本内容
- 用户内容块

**[助手消息]**

string

**[文本内容]**

**最少元素数：** `1`

回复工具调用时，将所有 `tool_result` 块放在文本块或图片块之前。

- Array [

oneOf

- 文本块
- 图片块
- 工具结果块

**[用户内容块]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[文本块]**

`deepseek-flash` 支持用户消息和工具结果中的图片输入，不支持 assistant 消息中的图片。`deepseek-v4-pro` 不支持图片输入。图片限制见[视觉理解指南](../guides/vision.md)。

**type** stringrequired

**Possible values:** `image`

**source** object

required

oneOf

- Base64 图片
- 图片 URL
- 已上传的图片文件

**[图片块]**

**type** stringrequired

**Possible values:** `base64`

**media\_type** stringrequired

**Possible values:** `image/jpeg`, `image/png`, `image/gif`, `image/webp`

**data** stringrequired

Base64 编码的图片数据，不包含 data URL 前缀。

**[工具结果块]**

**type** stringrequired

**Possible values:** `url`

**url** urirequired

服务端可下载图片的 HTTP 或 HTTPS URL。

**[Base64 图片]**

请求必须携带 `anthropic-beta: files-api-2025-04-14` 请求头。

**type** stringrequired

**Possible values:** `file`

**file\_id** stringrequired

已上传图片文件的 ID，见 [Files API 指南](../guides/files_api.md#anthropic-compatible-files-api)。

**[图片 URL]**

仅用于 user 消息。为每个待处理的工具调用 ID 返回一个结果，不得重复，并将结果放在所有文本块或图片块之前。

**type** stringrequired

**Possible values:** `tool_result`

**tool\_use\_id** stringrequired

紧接在前的 assistant 消息中对应 `tool_use` 块的 ID。

**content** string | object[] | null

nullable

工具输出，可以是字符串或文本、图片块数组。省略或为 `null` 时结果为空。

oneOf

- 文本内容
- 工具结果内容块
- 空值

**[已上传的图片文件]**

string

**[文本内容]**

- Array [

oneOf

- 文本块
- 图片块

**[工具结果内容块]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[空值]**

`deepseek-flash` 支持用户消息和工具结果中的图片输入，不支持 assistant 消息中的图片。`deepseek-v4-pro` 不支持图片输入。图片限制见[视觉理解指南](../guides/vision.md)。

**type** stringrequired

**Possible values:** `image`

**source** object

required

oneOf

- Base64 图片
- 图片 URL
- 已上传的图片文件

**[文本块]**

**type** stringrequired

**Possible values:** `base64`

**media\_type** stringrequired

**Possible values:** `image/jpeg`, `image/png`, `image/gif`, `image/webp`

**data** stringrequired

Base64 编码的图片数据，不包含 data URL 前缀。

**[图片块]**

**type** stringrequired

**Possible values:** `url`

**url** urirequired

服务端可下载图片的 HTTP 或 HTTPS URL。

**[Base64 图片]**

请求必须携带 `anthropic-beta: files-api-2025-04-14` 请求头。

**type** stringrequired

**Possible values:** `file`

**file\_id** stringrequired

已上传图片文件的 ID，见 [Files API 指南](../guides/files_api.md#anthropic-compatible-files-api)。

- ]

**[图片 URL]**

null

**is\_error** booleannullable

兼容字段，会被忽略。请在 `content` 中提供错误详情。

- ]

**[已上传的图片文件]**

历史 assistant 消息。回传时保留其内容块，包括思考、工具调用和网页搜索结果。

**role** stringrequired

**Possible values:** `assistant`

**content** string | object[]

required

oneOf

- 文本内容
- 助手内容块

**[文本内容]**

string

**[助手内容块]**

**最少元素数：** `1`

- Array [

oneOf

- 文本块
- 思考块
- 工具调用块
- 服务端工具调用块
- 网页搜索结果块

**[文本块]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[思考块]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

模型返回的思考内容。思考模式下继续工具调用轮次时，应原样回传。

**signature** stringnullable

思考块附带的签名。回传该块时应保留；输入签名目前不会被校验。

**[工具调用块]**

出现在 assistant 消息中。每个工具调用块都必须在紧接的 user 消息中有对应的工具结果块。

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

工具调用 ID，回传结果时作为 `tool_result.tool_use_id`。

**name** stringrequired

客户端工具名称。

**input** nullablerequired

传给工具的 JSON 参数，通常为符合其 `input_schema` 的对象。

**[服务端工具调用块]**

服务端执行网页搜索时返回。对应的 `web_search_tool_result` 出现在同一条 assistant 消息中，客户端无需执行该工具。

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

服务端工具调用 ID。

**name** stringrequired

**Possible values:** `web_search`

**input** nullablerequired

服务端工具参数，为 JSON 值，通常是 `{"query":"..."}` 这样的对象。回传 assistant 消息时应保留。

**caller**

object

标识直接调用的服务端工具。

**type** stringrequired

**Possible values:** `direct`

**[网页搜索结果块]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

关联的 `server_tool_use` 块 ID。

**content**

object[]

required

搜索结果或搜索错误项。随 assistant 消息回传时，应原样保留整个数组。

- Array [

oneOf

- 网页搜索结果
- 网页搜索错误

**[网页搜索结果]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

结果页面的标题。

**url** urirequired

结果页面的 URL。

**encrypted\_content** stringrequired

不可直接读取的结果内容。回传结果时应原样保留该值。

**page\_age** stringnullable

页面时效元数据（如有），可以为 `null`。

**[网页搜索错误]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

服务端搜索失败的原因。

- ]

- ]

- ]

**system** string | object[] | null

nullable

系统提示词，仅支持字符串、文本块数组或 `null`。

oneOf

- 文本内容
- 系统文本块
- 空值

**[文本内容]**

string

**[系统文本块]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

- Array [

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

- ]

**[空值]**

null

**max\_tokens** integernullable

**Possible values:** `>= 1`

请求的输出 token 上限，包括思考 token。HTTP API 中该字段可选，Anthropic SDK 则要求提供。默认值和有效上限取决于模型、思考模式与推理强度。超过模型上限的值会被截到上限，且输入与输出总长度不能超过上下文窗口。对于思考模式下的特定 Claude Code 或 OpenCode 主 Agent 请求，兼容处理可能在模型和上下文限制内将有效上限提高到请求值以上。详见[模型 & 价格](../quick_start/pricing.md)。

**stream** booleannullable

**Default value:** `false`

设为 `true` 时，以带事件名称的 SSE 返回结果，并以 `message_stop` 结束，不发送 `data: [DONE]`。否则返回一个完整的消息对象。

**thinking**

object

nullable

控制思考模式。显式设置的 `thinking.type` 在选择模式时优先于 `output_config.effort`。省略时由 `effort` 决定模式；两者均未设置时，`deepseek-flash` 和 `deepseek-v4-pro` 默认开启思考。

**type** stringrequired

**Possible values:** `enabled`, `disabled`, `adaptive`

`enabled` 开启思考，`disabled` 关闭思考；`adaptive` 按 `enabled` 处理。

**budget\_tokens** integernullable

**Possible values:** `>= 0`

兼容字段，会被忽略，不会设置思考 token 预算。

**output\_config**

object

nullable

输出配置。目前仅支持 `effort`，`format` 等输出格式设置会被忽略。

**effort** stringnullable

**Possible values:** `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `ultra`, `max`, `null`

控制思考模式与推理强度。`none` 关闭思考，但显式的 `thinking.type` 可以重新开启。`low`、`high` 和 `max` 开启思考，默认强度为 `high`。兼容别名：`minimal` 映射为 `low`，`medium` 和 `xhigh` 均映射为 `high`，`ultra` 映射为 `max`。显式设置的 `thinking.type` 决定是否开启思考。

**tools**

object[]

nullable

模型可使用的工具，支持客户端定义的工具和服务端网页搜索工具。工具名称必须唯一，空数组等同于未提供工具。`cache_control` 会被忽略。

- Array [

oneOf

- 客户端工具
- 网页搜索服务端工具

**[客户端工具]**

应用收到 `tool_use` 块后执行该工具，并返回 `tool_result` 块。客户端工具应省略 `type` 字段；提供 `type` 会按服务端工具解析，`custom` 等不支持的值会返回 `422`。`cache_control` 会被忽略。

**name** stringrequired

**最少字符数：** `1`

**最多字符数：** `128`

**Possible values:** Value must match regular expression `^[a-zA-Z0-9_-]+$`

唯一的工具名称，最多 128 个字符，仅可包含英文字母、数字、下划线或连字符。

**description** stringnullable

说明工具的用途及使用时机。

**input\_schema**

object

required

描述工具参数的有效 JSON Schema，顶层 `type` 必须为 `object`。

**property name\*** anynullable

**[网页搜索服务端工具]**

服务端执行网页搜索，并在 assistant 消息中返回 `server_tool_use` 和 `web_search_tool_result` 块。两个 type 值选择的是同一工具。

**type** stringrequired

**Possible values:** `web_search_20250305`, `web_search_20260209`

**name** stringrequired

**Possible values:** `web_search`

**max\_uses** integernullable

**Possible values:** `>= 0`

本次请求允许的最大搜索次数。默认值和服务端上限通常均为 5；Claude Code 搜索子 Agent 兼容请求的默认值和上限均为 1。超过相应上限的值会被截到上限。超过次数限制的搜索返回 `max_uses_exceeded` 结果。

- ]

**tool\_choice** object | null

nullable

控制工具选择，默认为 `auto`。`any` 按 `auto` 处理，不强制调用工具。指定客户端工具需要使用非思考模式。`disable_parallel_tool_use` 会被忽略。

oneOf

- 自动选择工具
- 任意工具（按自动选择处理）
- 指定工具
- 禁用工具调用
- 空值

**[自动选择工具]**

由模型决定是否调用工具，这是默认行为。

**type** stringrequired

**Possible values:** `auto`

**disable\_parallel\_tool\_use** booleannullable

兼容字段，会被忽略，不会禁用并行工具调用。

**[任意工具（按自动选择处理）]**

按 `auto` 处理，由模型决定是否调用工具。

**type** stringrequired

**Possible values:** `any`

**disable\_parallel\_tool\_use** booleannullable

兼容字段，会被忽略，不会禁用并行工具调用。

**[指定工具]**

选择指定工具。对于客户端工具，非思考模式下会强制调用，思考模式下则返回 `400` 错误。强制调用客户端工具时，请将 `thinking.type` 设为 `disabled`。

**type** stringrequired

**Possible values:** `tool`

**name** stringrequired

`tools` 中已提供的工具名称。

**disable\_parallel\_tool\_use** booleannullable

兼容字段，会被忽略，不会禁用并行工具调用。

**[禁用工具调用]**

禁用工具调用，即使请求中已提供 `tools`。

**type** stringrequired

**Possible values:** `none`

**[空值]**

null

**stop\_sequences** string[]nullable

**每个元素最少字符数：** `1`

**最多元素数：** `16`

最多 16 个非空停止字符串。匹配到其中一个字符串时，`stop_reason` 为 `stop_sequence`，`stop_sequence` 返回匹配的字符串。

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

采样温度，范围为 0 到 2。较高的值使输出更多样。思考模式下固定为 1，传入的值不生效。通常建议只调整此参数或 `top_p` 中的一个。

**top\_p** numbernullable

**Possible values:** `> 0` and `<= 1`

核采样概率，需大于 0 且不超过 1。`deepseek-flash` 在思考模式下默认为 1，小于 0.95 的值按 0.95 处理；非思考模式固定为 1。`deepseek-v4-pro` 在思考模式下启用工具时固定为 0.95，否则固定为 1，传入值被忽略；非思考模式使用传入值，默认为 1。将 `tool_choice` 设为 `{"type":"none"}` 会禁用工具调用。

**metadata**

object

nullable

请求元数据。仅支持 `user_id`，其它元数据字段会被忽略。

**user\_id** stringnullable

自定义终端用户标识。建议仅使用英文字母、数字、下划线（`_`）和连字符（`-`）。UTF-8 编码后不得超过 512 字节。请勿包含个人隐私信息。详见[限流与隔离](../quick_start/rate_limit.md)。

## Responses

- 200 (No streaming)
- 200 (Streaming)
- 400 (Bad request)

OK，返回一个 `message` 对象。内容可能包含文本、思考与工具调用内容块。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

此消息的唯一标识符。

**type** stringrequired

**Possible values:** `message`

**role** stringrequired

**Possible values:** `assistant`

**model** stringrequired

请求中提供的模型标识符。使用 Claude 兼容模型名时，响应保留该名称。

**content**

object[]

required

生成的内容块。在下一次请求中回传此 assistant 轮次时，请保留完整内容。

- Array [

oneOf

- 文本块
- 思考输出
- 工具调用块
- 服务端工具调用输出
- 网页搜索结果块

**[Example]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[文本块]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

生成的思考内容。在思考模式下继续工具调用对话时，请原样回传此内容块。

**signature** stringrequired

随思考内容块返回的不透明签名；回传内容块时请保留。

**[思考输出]**

出现在 assistant 消息中。每个工具调用块都必须在紧接的 user 消息中有对应的工具结果块。

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

工具调用 ID，回传结果时作为 `tool_result.tool_use_id`。

**name** stringrequired

客户端工具名称。

**input** nullablerequired

传给工具的 JSON 参数，通常为符合其 `input_schema` 的对象。

**[工具调用块]**

描述由服务端执行的一次工具调用。请求级搜索计数另见 `usage.server_tool_use`，客户端无需执行此调用。

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

服务端工具调用的标识符。

**name** stringrequired

服务端工具名称。

**input** nullablerequired

传递给服务端工具的参数，为 JSON 值，通常是对象。

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**[服务端工具调用输出]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

关联的 `server_tool_use` 块 ID。

**content**

object[]

required

搜索结果或搜索错误项。随 assistant 消息回传时，应原样保留整个数组。

- Array [

oneOf

- 网页搜索结果
- 网页搜索错误

**[网页搜索结果块]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

结果页面的标题。

**url** urirequired

结果页面的 URL。

**encrypted\_content** stringrequired

不可直接读取的结果内容。回传结果时应原样保留该值。

**page\_age** stringnullable

页面时效元数据（如有），可以为 `null`。

**[网页搜索结果]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

服务端搜索失败的原因。

- ]

- ]

**stop\_reason** stringnullablerequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`, `null`

生成停止的原因：自然结束、达到输出上限、命中停止序列、调用客户端工具或内容过滤。在 message\_start 中为 null。

**stop\_sequence** stringnullablerequired

命中的停止序列；未命中时为 null。

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

未命中上下文缓存的输入 token 数。总输入 token 数为 input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens。

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

固定为 0。不使用 Anthropic 式的缓存创建机制；上下文缓存由服务端自动管理。

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

命中上下文缓存的输入 token 数。

**output\_tokens** integerrequired

**Possible values:** `>= 0`

生成的输出 token 数，开启思考时包含思考 token。在 message\_delta 中为累计值，而非增量。

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

服务端网页搜索次数，与 token 用量分别统计。仅在至少尝试过一次网页搜索时返回，否则省略整个字段。返回时两个子字段均存在。非流式响应读取最终消息的 usage，流式响应读取最后的 message\_delta.usage。这些计数是累计值，不是增量。详见[服务端工具用量](../guides/anthropic_api.md#server-tool-usage)。

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

服务端网页搜索尝试次数，包括失败和超过 `max_uses` 限制的尝试。

**tool\_search** integerrequired

**Possible values:** `>= 0`

成功且返回非空结果的服务端网页搜索次数。失败或结果为空的尝试不计入。此字段可作为计费依据。

**[网页搜索错误]**

```json
{
  "id": "e6ef6a63-a078-4f53-a73b-38c8d1d46310",
  "type": "message",
  "role": "assistant",
  "model": "deepseek-flash",
  "content": [{"type": "text", "text": "Hello!"}],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 3,
    "service_tier": "standard"
  }
}
```

OK，依次返回 `message_start` → 内容块事件 → `message_delta` → `message_stop` SSE 事件。事件间可能穿插 `ping` 事件或保活注释。不会发送 `data: [DONE]`。工具输入的 JSON 片段需先拼接，在内容块结束后再解析。详见[流式输出](../guides/anthropic_api.md#streaming)。

在收到 `message_stop` 前连接关闭，表示响应不完整。流式输出开始后发生的错误可能直接终止连接，不一定发送 Anthropic `error` 事件。

**[text/event-stream]**

- Schema
- Example

**[Schema]**

**Schema**

正常消息事件的 event 名称与 JSON 的 type 相同。正常流以 message\_stop 结束。事件间可能穿插 ping 或保活注释；不会发送 data: [DONE]。超时时可能返回一条包含 error 对象、没有事件名称的 data 事件，随后关闭连接。未收到 message\_stop 就中断的流是不完整的。

- Array [

oneOf

- message\_start
- content\_block\_start
- content\_block\_delta
- content\_block\_stop
- message\_delta
- message\_stop
- ping

**[Example]**

**type** stringrequired

**Possible values:** `message_start`

**message**

object

required

**id** stringrequired

此消息的唯一标识符。

**type** stringrequired

**Possible values:** `message`

**role** stringrequired

**Possible values:** `assistant`

**model** stringrequired

请求中提供的模型标识符。使用 Claude 兼容模型名时，响应保留该名称。

**content**

object[]

required

生成的内容块。在下一次请求中回传此 assistant 轮次时，请保留完整内容。

- Array [

oneOf

- 文本块
- 思考输出
- 工具调用块
- 服务端工具调用输出
- 网页搜索结果块

**[message\_start]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[content\_block\_start]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

生成的思考内容。在思考模式下继续工具调用对话时，请原样回传此内容块。

**signature** stringrequired

随思考内容块返回的不透明签名；回传内容块时请保留。

**[content\_block\_delta]**

出现在 assistant 消息中。每个工具调用块都必须在紧接的 user 消息中有对应的工具结果块。

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

工具调用 ID，回传结果时作为 `tool_result.tool_use_id`。

**name** stringrequired

客户端工具名称。

**input** nullablerequired

传给工具的 JSON 参数，通常为符合其 `input_schema` 的对象。

**[content\_block\_stop]**

描述由服务端执行的一次工具调用。请求级搜索计数另见 `usage.server_tool_use`，客户端无需执行此调用。

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

服务端工具调用的标识符。

**name** stringrequired

服务端工具名称。

**input** nullablerequired

传递给服务端工具的参数，为 JSON 值，通常是对象。

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**[message\_delta]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

关联的 `server_tool_use` 块 ID。

**content**

object[]

required

搜索结果或搜索错误项。随 assistant 消息回传时，应原样保留整个数组。

- Array [

oneOf

- 网页搜索结果
- 网页搜索错误

**[message\_stop]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

结果页面的标题。

**url** urirequired

结果页面的 URL。

**encrypted\_content** stringrequired

不可直接读取的结果内容。回传结果时应原样保留该值。

**page\_age** stringnullable

页面时效元数据（如有），可以为 `null`。

**[ping]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

服务端搜索失败的原因。

- ]

- ]

**stop\_reason** stringnullablerequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`, `null`

生成停止的原因：自然结束、达到输出上限、命中停止序列、调用客户端工具或内容过滤。在 message\_start 中为 null。

**stop\_sequence** stringnullablerequired

命中的停止序列；未命中时为 null。

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

未命中上下文缓存的输入 token 数。总输入 token 数为 input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens。

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

固定为 0。不使用 Anthropic 式的缓存创建机制；上下文缓存由服务端自动管理。

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

命中上下文缓存的输入 token 数。

**output\_tokens** integerrequired

**Possible values:** `>= 0`

生成的输出 token 数，开启思考时包含思考 token。在 message\_delta 中为累计值，而非增量。

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

服务端网页搜索次数，与 token 用量分别统计。仅在至少尝试过一次网页搜索时返回，否则省略整个字段。返回时两个子字段均存在。非流式响应读取最终消息的 usage，流式响应读取最后的 message\_delta.usage。这些计数是累计值，不是增量。详见[服务端工具用量](../guides/anthropic_api.md#server-tool-usage)。

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

服务端网页搜索尝试次数，包括失败和超过 `max_uses` 限制的尝试。

**tool\_search** integerrequired

**Possible values:** `>= 0`

成功且返回非空结果的服务端网页搜索次数。失败或结果为空的尝试不计入。此字段可作为计费依据。

**[文本块]**

**type** stringrequired

**Possible values:** `content_block_start`

**index** integerrequired

**Possible values:** `>= 0`

内容块的索引，从 0 开始。

**content\_block** object

required

oneOf

- 文本块
- 思考输出
- 工具调用块
- 服务端工具调用输出
- 网页搜索结果块

**[思考输出]**

每个文本块的 `type` 必须为 `"text"`，内容放在 `text` 字段中。请求中额外传入的 `cache_control` 和 `citations` 字段会被忽略。

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

文本内容。

**[工具调用块]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

生成的思考内容。在思考模式下继续工具调用对话时，请原样回传此内容块。

**signature** stringrequired

随思考内容块返回的不透明签名；回传内容块时请保留。

**[服务端工具调用输出]**

出现在 assistant 消息中。每个工具调用块都必须在紧接的 user 消息中有对应的工具结果块。

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

工具调用 ID，回传结果时作为 `tool_result.tool_use_id`。

**name** stringrequired

客户端工具名称。

**input** nullablerequired

传给工具的 JSON 参数，通常为符合其 `input_schema` 的对象。

**[网页搜索结果块]**

描述由服务端执行的一次工具调用。请求级搜索计数另见 `usage.server_tool_use`，客户端无需执行此调用。

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

服务端工具调用的标识符。

**name** stringrequired

服务端工具名称。

**input** nullablerequired

传递给服务端工具的参数，为 JSON 值，通常是对象。

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**[网页搜索结果]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

关联的 `server_tool_use` 块 ID。

**content**

object[]

required

搜索结果或搜索错误项。随 assistant 消息回传时，应原样保留整个数组。

- Array [

oneOf

- 网页搜索结果
- 网页搜索错误

**[网页搜索错误]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

结果页面的标题。

**url** urirequired

结果页面的 URL。

**encrypted\_content** stringrequired

不可直接读取的结果内容。回传结果时应原样保留该值。

**page\_age** stringnullable

页面时效元数据（如有），可以为 `null`。

**[文本块]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

服务端搜索失败的原因。

- ]

**[思考输出]**

**type** stringrequired

**Possible values:** `content_block_delta`

**index** integerrequired

**Possible values:** `>= 0`

内容块的索引，从 0 开始。

**delta** object

required

oneOf

- 文本增量
- 思考增量
- 签名增量
- 工具输入增量

**[工具调用块]**

**type** stringrequired

**Possible values:** `text_delta`

**text** stringrequired

将此文本追加到当前文本内容块。

**[服务端工具调用输出]**

**type** stringrequired

**Possible values:** `thinking_delta`

**thinking** stringrequired

将此文本追加到当前思考内容块。

**[网页搜索结果块]**

**type** stringrequired

**Possible values:** `signature_delta`

**signature** stringrequired

已完成的思考内容块的签名。

**[网页搜索结果]**

**type** stringrequired

**Possible values:** `input_json_delta`

**partial\_json** stringrequired

工具输入 JSON 的一个片段。拼接此内容块的全部片段，在 content\_block\_stop 后解析完整 JSON。

**[网页搜索错误]**

**type** stringrequired

**Possible values:** `content_block_stop`

**index** integerrequired

**Possible values:** `>= 0`

内容块的索引，从 0 开始。

**[文本增量]**

**type** stringrequired

**Possible values:** `message_delta`

**delta**

object

required

**stop\_reason** stringrequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`

生成停止的最终原因。

**stop\_sequence** stringnullablerequired

命中的停止序列；未命中时为 null。

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

未命中上下文缓存的输入 token 数。总输入 token 数为 input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens。

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

固定为 0。不使用 Anthropic 式的缓存创建机制；上下文缓存由服务端自动管理。

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

命中上下文缓存的输入 token 数。

**output\_tokens** integerrequired

**Possible values:** `>= 0`

生成的输出 token 数，开启思考时包含思考 token。在 message\_delta 中为累计值，而非增量。

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

服务端网页搜索次数，与 token 用量分别统计。仅在至少尝试过一次网页搜索时返回，否则省略整个字段。返回时两个子字段均存在。非流式响应读取最终消息的 usage，流式响应读取最后的 message\_delta.usage。这些计数是累计值，不是增量。详见[服务端工具用量](../guides/anthropic_api.md#server-tool-usage)。

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

服务端网页搜索尝试次数，包括失败和超过 `max_uses` 限制的尝试。

**tool\_search** integerrequired

**Possible values:** `>= 0`

成功且返回非空结果的服务端网页搜索次数。失败或结果为空的尝试不计入。此字段可作为计费依据。

**[思考增量]**

**type** stringrequired

**Possible values:** `message_stop`

**[签名增量]**

**type** stringrequired

**Possible values:** `ping`

- ]

**[工具输入增量]**

```shell
event: message_start
data: {"type":"message_start","message":{"id":"e6ef6a63-a078-4f53-a73b-38c8d1d46310","type":"message","role":"assistant","model":"deepseek-flash","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":12,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":0,"service_tier":"standard"}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type":"ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello!"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"input_tokens":12,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":3,"service_tier":"standard"}}

event: message_stop
data: {"type":"message_stop"}
```

无效请求，例如 `messages` 数组为空或工具结果未配对。请求错误使用 DeepSeek 通用的 `{error: {message, type, param, code}}` 结构，不含 Anthropic 顶层的 `type: "error"` 字段。其他 HTTP 错误请参考[错误码](../quick_start/error_codes.md)。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**error**

object

required

**code** stringnullablerequired

**message** stringrequired

**param** stringnullablerequired

**type** stringrequired

**[Example]**

```json
{
  "error": {
    "message": "messages: at least one message is required",
    "type": "invalid_request_error",
    "param": null,
    "code": "invalid_request_error"
  }
}
```

Loading...
