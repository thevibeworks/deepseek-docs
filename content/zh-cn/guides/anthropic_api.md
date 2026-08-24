---
title: "使用 Anthropic API"
description: "为了满足大家对 Anthropic API 生态的使用需求，我们的 API 新增了对 Anthropic API 格式的支持，其 base_url 为 https://api.deepseek.com/anthropic。"
source: https://api-docs.deepseek.com/zh-cn/guides/anthropic_api
fetched: 2026-08-23
---

# 使用 Anthropic API

为了满足大家对 Anthropic API 生态的使用需求，我们的 API 新增了对 Anthropic API 格式的支持，其 `base_url` 为 `https://api.deepseek.com/anthropic`。

通过简单的配置，即可将 DeepSeek 的能力，接入到 Anthropic API 生态中。

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
    model="deepseek-v4-pro",
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

**注意**：当您给 DeepSeek 的 Anthropic API 传入不支持的模型名时，API 后端会自动将其映射到 `deepseek-v4-flash` 模型。

---

## Anthropic 模型映射

您在使用 Anthropic API 时，我们会对您传入的 claude 模型名进行映射：

- claude-opus 开头的模型，会映射到 deepseek-v4-pro
- claude-haiku、claude-sonnet 开头的模型，会映射到 deepseek-v4-flash

通过这样的映射，您在使用新版 Claude Desktop APP 的 developer 模式时，可以绕过 APP 对模型名的限制，只需改动 base\_url 和 api\_key，即可在其中接入 DeepSeek 模型。

---

## Anthropic API 兼容性细节

本小节罗列了 DeepSeek API 对 Anthropic API 的兼容性细节。Anthropic API 完整格式定义，请参考 [Anthropic 官方 API 手册](https://platform.claude.com/docs/en/api/python/beta/messages/create)。

### HTTP Header

| 字段 | 支持情况 |
| --- | --- |
| anthropic-beta | `/messages` 忽略；Files API 端点必须携带（`files-api-2025-04-14`）——见 [Files API](files_api.md#anthropic-compatible-files-api) |
| anthropic-version | 忽略 |
| x-api-key | 完全支持 |

### 简单字段

| 字段 | 支持情况 |
| --- | --- |
| model | 改为使用 DeepSeek 模型 |
| max\_tokens | 完全支持 |
| container | 忽略 |
| mcp\_servers | 忽略 |
| metadata | 支持 `user_id`，其它字段忽略 关于 `user_id` 参数的更多信息，请参考 [限速与隔离](../quick_start/rate_limit.md)。 |
| service\_tier | 忽略 |
| stop\_sequences | 完全支持 |
| stream | 完全支持 |
| system | 完全支持 |
| temperature | 完全支持（范围 [0.0 ~ 2.0]） |
| thinking | 支持（`budget_tokens` 被忽略） |
| output\_config | 仅支持 `effort` |
| top\_k | 忽略 |
| top\_p | 完全支持 |

### Tool 字段

#### tools

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
| any | 支持（`disable_parallel_tool_use` 被忽略） |
| tool | 支持（`disable_parallel_tool_use` 被忽略） |

### Message 字段

| 字段 | 变体 | 子字段 | 支持情况 |
| --- | --- | --- | --- |
| content | string |  | 完全支持 |
| array, type="text" | text | 完全支持 |
| cache\_control | 忽略 |
| citations | 忽略 |
| array, type="image" | source | 支持。`source.type` 可为 base64（媒体类型：jpeg、png、gif、webp）、url 或 file（file 形式需带请求头 `anthropic-beta: files-api-2025-04-14`） |
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
