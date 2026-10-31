---
title: "使用 Anthropic API"
description: "为了满足大家对 Anthropic API 生态的使用需求，我们的 API 新增了对 Anthropic API 格式的支持，其 base_url 为 https://api.deepseek.com/anthropic。"
source: https://api-docs.deepseek.com/zh-cn/guides/anthropic_api
fetched: 2026-10-31
---

# 使用 Anthropic API

为了满足大家对 Anthropic API 生态的使用需求，我们的 API 新增了对 Anthropic API 格式的支持，其 `base_url` 为 `https://api.deepseek.com/anthropic`。

通过简单的配置，即可将 DeepSeek 的能力，接入到 Anthropic API 生态中。

请求参数、响应字段和完整 HTTP 示例请参考 [Messages API 参考文档](../api/create-message.md)。

---

## 将 DeepSeek 模型接入 Claude Code

请参考[接入 Claude Code](../quick_start/agent_integrations/claude_code.md)

## 通过 Anthropic API 调用 DeepSeek 模型

1. 安装 Anthropic SDK

```text
pip install anthropic
```

2. 配置环境变量

```text
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

3. 调用 API

```text
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="deepseek-flash",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi, how are you?"
                }
            ]
        }
    ]
)
print(message.content)
```

**注意**：以 `claude` 开头的不支持的模型名仍会被接受：`claude-opus*` 会映射到 `deepseek-v4-pro`，其它 `claude*` 模型名会映射到 `deepseek-flash`。不以 `claude` 开头的未知模型名会返回 `400` 错误。

---

## Anthropic 模型映射

您在使用 Anthropic API 时，我们会对您传入的 claude 模型名进行映射：

- claude-opus 开头的模型，会映射到 `deepseek-v4-pro`
- claude-haiku、claude-sonnet 开头的模型，会映射到 `deepseek-flash`

claude-opus 映射到的 `deepseek-v4-pro` 按 V4 Pro 价格计费。

通过这样的映射，您在使用新版 Claude Desktop APP 的 developer 模式时，可以绕过 APP 对模型名的限制，只需改动 base\_url 和 api\_key，即可在其中接入 DeepSeek 模型。

---

## Anthropic API 兼容性细节

本小节罗列了 DeepSeek API 对 Anthropic API 的兼容性细节。Anthropic API 完整格式定义，请参考 [Anthropic 官方 API 手册](https://platform.claude.com/docs/en/api/python/beta/messages/create)。

### HTTP Header

使用 `x-api-key: <API_KEY>` 或 `Authorization: Bearer <API_KEY>` 中的任一种方式鉴权。

| 字段 | 支持情况 |
| --- | --- |
| anthropic-beta | `/messages` 忽略；但 `source.type` 为 `file` 的图片必须携带（`files-api-2025-04-14`）；Files API 端点必须携带——见 [Files API](files_api.md#anthropic-compatible-files-api) |
| anthropic-version | 忽略 |
| x-api-key | 完全支持 |
| Authorization | 支持 `Bearer <API_KEY>`，可替代 `x-api-key` |

### 简单字段

| 字段 | 支持情况 |
| --- | --- |
| model | 改为使用 DeepSeek 模型 |
| max\_tokens | 支持。在 HTTP 请求中可省略，默认值和有效上限取决于模型、思考模式与推理强度。Anthropic SDK 要求提供此参数，因此 SDK 示例显式设置该值。兼容场景的例外见下文 |
| container | 忽略 |
| mcp\_servers | 忽略 |
| metadata | 支持 `user_id`，其它字段忽略 关于 `user_id` 参数的更多信息，请参考 [限速与隔离](../quick_start/rate_limit.md)。 |
| service\_tier | 忽略 |
| stop\_sequences | 完全支持 |
| stream | 完全支持 |
| system | 完全支持 |
| temperature | 有效范围为 [0.0 ~ 2.0]。非思考模式下生效；思考模式下固定为 `1.0` |
| thinking | 支持 `type: "enabled"` 和 `type: "disabled"`；`adaptive` 按 `enabled` 处理。`budget_tokens` 被忽略 |
| output\_config | 仅支持 `effort` |
| top\_k | 忽略 |
| top\_p | 因模型而异： `deepseek-flash`：思考模式下生效（下限 `0.95`），非思考模式下恒为 `1.0`。 `deepseek-v4-pro`：思考模式下忽略传入值（启用工具调用时固定为 `0.95`，否则为 `1.0`），非思考模式下生效。即使提供了 `tools`，将 `tool_choice` 设为 `{"type": "none"}` 也会关闭工具调用 |

在部分 Claude Code 或 OpenCode 主 Agent 的思考模式请求中，兼容处理可能将实际生效的 `max_tokens` 提高到请求值以上。在这些场景下，不能依靠此参数严格限制输出 token 数。

### Tool 字段

#### tools

定义客户端工具时，提供 `name`、`input_schema` 和可选的 `description`，不要传入 `type`。`type` 用于选择服务端工具；为客户端工具传入 `type: "custom"` 会返回 `422` 错误。

| 字段 | 支持情况 |
| --- | --- |
| name | 完全支持 |
| input\_schema | 完全支持 |
| description | 完全支持 |
| cache\_control | 忽略 |

#### tool\_choice

| 取值 | 支持情况 |
| --- | --- |
| none | 完全支持 |
| auto | 支持（`disable_parallel_tool_use` 被忽略） |
| any | 按 `auto` 处理，不强制调用工具（`disable_parallel_tool_use` 被忽略） |
| tool | 非思考模式下指定客户端工具；思考模式下返回 `400` 错误（`disable_parallel_tool_use` 被忽略） |

#### 回传工具结果

多轮对话需要在每次请求的 `messages` 中发送对话历史。如果 assistant 消息包含客户端 `tool_use`，紧接着的消息必须为 `user`，并为全部工具调用提供 `tool_use_id` 对应的 `tool_result`。该 user 消息中的所有 `tool_result` 块必须放在文本之前。

在思考模式下继续工具调用时，建议原样保留并回传 assistant 的完整 `content` 数组，包括 `thinking` 和工具调用块。遗漏思考内容时，服务端可能根据工具调用 ID 恢复；需要恢复但无法恢复时，请求会返回 `400` 错误。请勿依赖自动恢复。

### Message 字段

| 字段 | 变体 | 子字段 | 支持情况 |
| --- | --- | --- | --- |
| content | string |  | 完全支持 |
| array, type="text" | text | 完全支持 |
| cache\_control | 忽略 |
| citations | 忽略 |
| array, type="image" | source | `deepseek-flash` 支持 user 消息和 `tool_result` 内容中的图片；assistant 消息中的图片会返回 `400` 错误。`deepseek-v4-pro` 不处理图片，会将其替换为文本 `[Unsupported Image]`。 `source.type` 可为 base64（媒体类型：image/jpeg、image/png、image/gif、image/webp）、url 或 file（使用 file 图片时，请携带请求头 `anthropic-beta: files-api-2025-04-14`）。 |
| array, type = "document" |  | 不支持 |
| array, type = "search\_result" |  | 不支持 |
| array, type = "thinking" |  | 支持 |
| array, type="redacted\_thinking" |  | 不支持 |
| array, type = "tool\_use" | id | 完全支持 |
| input | 完全支持 |
| name | 完全支持 |
| cache\_control | 忽略 |
| array, type = "tool\_result" | tool\_use\_id | 完全支持 |
| content | 完全支持 |
| cache\_control | 忽略 |
| is\_error | 忽略 |
| array, type = "server\_tool\_use" |  | 支持 |
| array, type = "web\_search\_tool\_result" |  | 支持 |
| array, type = "code\_execution\_tool\_result" |  | 不支持 |
| array, type = "mcp\_tool\_use" |  | 不支持 |
| array, type = "mcp\_tool\_result" |  | 不支持 |
| array, type = "container\_upload" |  | 不支持 |

## 服务端工具用量

`type: "server_tool_use"` 的内容块表示由服务端执行的工具调用，包含调用 `id`、工具 `name`、JSON 参数 `input` 和调用方 `caller`。网页搜索的 `name` 为 `web_search`，`input` 中包含搜索词 `query`，`caller` 为 `{"type":"direct"}`。对应的 `web_search_tool_result` 块通过 `tool_use_id` 引用同一个调用 ID。服务端执行搜索后会继续生成回答，客户端无需执行该工具，也无需提供 `tool_result`。

`usage.server_tool_use` 统计本次请求中的搜索调用：

| 字段 | 含义 |
| --- | --- |
| `web_search_requests` | 尝试发起的服务端网页搜索次数，包括因超过 `max_uses` 被拒绝、查询无效或搜索失败的调用。因此，该值可能大于 `max_uses`。 |
| `tool_search` | 搜索成功且至少返回一条结果的网页搜索次数。搜索失败或结果为空时不增加。统计单位是调用次数，而不是搜索结果条数。 |

本次没有尝试网页搜索时，会省略该对象；仅在 `tools` 中声明搜索工具，并不保证它会出现。非流式响应读取 `usage.server_tool_use`；流式响应读取最后一个 `message_delta.usage.server_tool_use` 中的累计值，初始 `message_start` 的用量不包含这些计数。

例如，使用 DeepSeek API key 向 `POST /anthropic/v1/messages` 发送以下请求体：

```json
{
  "model": "deepseek-v4-pro",
  "max_tokens": 256,
  "thinking": {"type": "disabled"},
  "tools": [
    {"type": "web_search_20250305", "name": "web_search", "max_uses": 1}
  ],
  "messages": [
    {
      "role": "user",
      "content": "Use the web search tool once to search for Python official website. Then reply with only the official site URL."
    }
  ]
}
```

该请求的一次成功响应包含 `server_tool_use`、`web_search_tool_result` 和 `text` 内容块，用量摘录如下。不同请求的 token 数和搜索次数可能不同。

```json
{
  "usage": {
    "input_tokens": 2912,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 256,
    "output_tokens": 52,
    "service_tier": "standard",
    "server_tool_use": {
      "web_search_requests": 1,
      "tool_search": 1
    }
  }
}
```

## 流式输出与 Token 用量

将 `stream` 设为 `true` 后，接口以 SSE 事件返回结果。正常响应以 `message_start` 开始，各内容块依次发送 `content_block_start`、`content_block_delta` 和 `content_block_stop`，最后发送 `message_delta` 和 `message_stop`。期间可能穿插 `ping` 事件。流中没有 `data: [DONE]` 消息。

正常消息事件具有 SSE `event` 名称和 JSON `type` 字段，流中也可能出现保活注释。如果等待生成开始超时，服务端可能发送一个包含 `{"error":{"message":"..."}}` 的无名 `data` 帧，其中没有 SSE `event` 名称或顶层 JSON `type`，随后关闭连接。在收到 `message_stop` 前连接关闭，表示响应不完整。

以最后的 `message_delta.usage` 作为本次请求的 Token 用量，不要与 `message_start` 中的初始用量相加。`input_tokens` 不含缓存命中的 Token，`cache_read_input_tokens` 表示缓存命中量，`cache_creation_input_tokens` 目前恒为 `0`。总输入 Token 数为 `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`。

响应示例和错误处理请参考 [Messages API 参考文档](../api/create-message.md)。
