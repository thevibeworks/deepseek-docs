---
title: "使用 Responses API"
description: "为了满足大家对 Codex 的需求，我们的 API 新增了对 Responses API 格式的支持，其 base_url 为 https://api.deepseek.com。"
source: https://api-docs.deepseek.com/zh-cn/guides/responses_api
fetched: 2026-10-31
---

# 使用 Responses API

为了满足大家对 Codex 的需求，我们的 API 新增了对 Responses API 格式的支持，其 `base_url` 为 `https://api.deepseek.com`。

通过简单的配置，即可在 Codex 中使用 DeepSeek 模型。

## 将 DeepSeek 模型接入 Codex

请参考[接入 Codex](../quick_start/agent_integrations/codex.md)

## 通过 Responses API 调用 DeepSeek 模型

```python
# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="<your DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.responses.create(
    model="deepseek-flash",
    instructions="You are a helpful assistant.",
    input="Hi, how are you?",
)

print(response.output_text)
```

## 流式输出

设置 `stream: true`，响应将以语义化的流式 SSE 事件序列返回。每个事件带有表示事件类型的 `event` 字段和递增的 `sequence_number`。流以 `response.completed` / `response.incomplete` / `response.failed` 事件结束，没有 `data: [DONE]` 消息。

```python
stream = client.responses.create(
    model="deepseek-flash",
    instructions="You are a helpful assistant.",
    input="Hi, how are you?",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
```

完整事件列表：

| 事件 | 说明 |
| --- | --- |
| `response.created` | 首个事件；响应已创建，状态为 `in_progress` |
| `response.in_progress` | 响应正在生成中 |
| `response.output_item.added` / `response.output_item.done` | 一个输出 item（`reasoning` / `message` / `function_call` / `custom_tool_call` / `web_search_call` / `tool_search_call`）开始 / 完成 |
| `response.content_part.added` / `response.content_part.done` | 输出 item 中的一个内容块开始 / 完成 |
| `response.reasoning_text.delta` / `response.reasoning_text.done` | 思维链文本增量 / 完整思维链文本 |
| `response.output_text.delta` / `response.output_text.done` | 输出文本增量 / 完整输出文本 |
| `response.function_call_arguments.delta` / `response.function_call_arguments.done` | Function 调用参数增量 / 完整参数 |
| `response.custom_tool_call_input.delta` / `response.custom_tool_call_input.done` | Custom 工具调用（`apply_patch`）输入增量 / 完整输入 |
| `response.web_search_call.in_progress` / `response.web_search_call.searching` / `response.web_search_call.completed` | 服务端 `web_search` 调用开始 / 搜索中 / 完成（仅 `deepseek-v4-pro`） |
| `response.completed` | 响应正常完成时的最后一个事件，携带包含 `usage` 的完整 `response` 对象 |
| `response.incomplete` | 响应被截断（如达到 `max_output_tokens`）时的最后一个事件，携带完整 `response` 对象 |
| `response.failed` | 响应失败时的最后一个事件，携带含 `error` 详情的完整 `response` 对象 |

## 图片输入

Responses API 支持使用 `deepseek-flash` 模型传入图片，适用的图片限制与支持格式与[对话补全](vision.md#limits)一致。

图片通过 `message` item 中的 `input_image` 内容块提供，使用 `image_url`（`http(s)` URL 或 base64 data URL）或 `file_id`（通过 [Files API](files_api.md) 上传的图片）二者之一：

```python
response = client.responses.create(
    model="deepseek-flash",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "这张图片里有什么？"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg", "detail": "low"},
            ],
        },
    ],
)
print(response.output_text)
```

`input_image` 内容块也可以出现在 `function_call_output` / `custom_tool_call_output` item 的 `output` 中，让模型接收你的工具生成的图片：

```python
input=[
    {"role": "user", "content": "读取工具返回的截图。"},
    {"type": "function_call", "call_id": "fc1", "name": "take_screenshot", "arguments": "{}"},
    {"type": "function_call_output", "call_id": "fc1",
     "output": [{"type": "input_image", "image_url": "data:image/png;base64,<BASE64_DATA>"}]},
]
```

### `input_image` 字段

- `image_url`：图片的 `http(s)` URL（最多 8192 个字符）或 base64 编码的 data URL（`data:image/jpeg;base64,...`）。支持的格式：JPEG、PNG、GIF、WebP。
- `file_id`：通过 [Files API](files_api.md) 上传的图片文件 ID，形如 `file-api-...`。
- `detail`：`low` / `high` / `original` / `auto`。`low` 在推理前将图片缩小到 512x512；其余取值保留原图。设置 `file_id` 时被忽略。

`image_url` 与 `file_id` 互斥：两者都不传返回 `400` 错误（"input\_image must have image\_url or file\_id"），两者都传返回 `400` 错误（"input\_image cannot have both image\_url and file\_id"）。

### 使用限制

- 图片仅允许出现在 `user` / `developer` 消息 item 以及 `function_call_output` / `custom_tool_call_output` 的输出中；`system` / `assistant` 消息中的图片会返回 `400` 错误。
- `deepseek-flash` 会真正处理 `input_image` 内容块。
- 与对话补全相同的图片限制（内联单张 32 MiB、`file_id` 单张 64 MiB、不含 `file_id` 图片总计 64 MiB，含 `file_id` 图片最高 200 MiB、单请求 600 张等）同样适用，详见[图像理解：限制](vision.md#limits)。

## 兼容性明细

本小节罗列了 DeepSeek API 对 Responses API 的兼容性细节。Responses API 完整格式定义，请参考 [OpenAI 官方 API 手册](https://developers.openai.com/api/reference/resources/responses/methods/create)。

### 顶层请求参数

| 参数 | 支持情况 |
| --- | --- |
| `model` | 支持。`deepseek-flash` 和 `deepseek-v4-pro`，见[模型 & 价格](../quick_start/pricing.md) |
| `input` | 支持。字符串或输入 item 列表；`input` 与 `instructions` 至少传一个 |
| `instructions` | 支持。作为第一条 system 消息 |
| `stream` | 支持 |
| `temperature` | 支持（范围 [0.0, 2.0]；思考模式下不生效） |
| `top_p` | 支持；行为因模型而异： `deepseek-flash`：思考模式下生效（下限 `0.95`），非思考模式下恒为 `1.0`。 `deepseek-v4-pro`：思考模式下忽略传入值（启用工具调用时固定为 `0.95`，否则为 `1.0`），非思考模式下生效。即使提供了 `tools`，将 `tool_choice` 设为 `none` 也会关闭工具调用 |
| `max_output_tokens` | 支持 |
| `top_logprobs` | 支持（范围 [0, 20]） |
| `tools` | 部分支持。`function` 支持；`web_search` 在 `deepseek-v4-pro` 下支持；其他类型忽略，见下方 Tools 表 |
| `tool_choice` | 支持。`none` / `auto` / `required` / 指定某个工具（`{"type": "function", "name": ...}`） |
| `reasoning` | 部分支持。`effort` 支持；`summary` 可传入但不生成摘要 |
| `text` | 部分支持。`format` 完整支持；`verbosity` 可传入但不生效 |
| `user` | 支持。参考[限速与用户隔离](../quick_start/rate_limit.md) |
| `parallel_tool_calls` | 忽略（并行工具调用始终开启） |
| `max_tool_calls` | 忽略 |
| `previous_response_id` | 不支持（无状态 API） |
| `conversation` | 不支持（无状态 API） |
| `store` | 不支持。响应中恒为 `store: false` |
| `background` | 不支持 |
| `metadata` | 不支持 |
| `include` | 不支持 |
| `prompt` | 不支持 |
| `truncation` | 不支持。输入超出上下文窗口时返回 `400` 错误 |
| `service_tier` | 不支持 |
| `safety_identifier` | 不支持 |
| `prompt_cache_key` / `prompt_cache_retention` | 不支持。上下文缓存自动管理，见[上下文硬盘缓存](kv_cache.md) |
| `context_management` | 不支持 |
| `stream_options` | 不支持 |

不支持的参数会被**静默忽略**、不会报错，因此现有的 Responses API 客户端无需修改即可接入。

### 输入 Items

| 类型 | 支持情况 |
| --- | --- |
| `message` | 支持。角色支持 `user` / `assistant` / `system` / `developer`（`developer` 视同 `user`）；content 支持字符串和 `input_text` / `output_text` / `input_image` 内容块。`input_image` 内容块会作为真实图片处理（仅允许出现在 `user` / `developer` 消息中，`system` / `assistant` 消息中的图片会返回 `400` 错误）。文件输入不支持 |
| `function_call` | 支持。归并到相邻 assistant 消息 |
| `function_call_output` | 支持。`output` 可以是字符串或内容块列表；输出中的 `input_image` 内容块会作为真实图片处理 |
| `reasoning` | 支持。明文 `content` 归并到相邻 assistant 消息；`summary`、`encrypted_content` 不支持 |
| `custom_tool_call` / `custom_tool_call_output` | 支持（配合 `apply_patch` custom 工具使用，含 `call_id` 配对校验）。`output` 中的 `input_image` 内容块会作为真实图片处理 |
| 其他类型 | 忽略 |

注：上一次响应返回的 `web_search_call` item 可以回传到 `input`，接口会还原对应的搜索结果并拼接到上下文中。

### Tools

| 类型 | 支持情况 |
| --- | --- |
| `function` | 支持 |
| `custom` | 仅支持 `{"type": "custom", "name": "apply_patch"}`（用于 Codex 兼容）；其他名称返回 `400` 错误 |
| `web_search` | `deepseek-v4-pro` 支持。接口会在服务端执行搜索，将结果加入上下文并继续生成响应；`deepseek-flash` 下忽略 |
| `file_search` / `code_interpreter` / `computer_use` / `mcp` 等内置工具 | 忽略 |

### 响应字段

响应对象与 OpenAI Responses API 的 `response` 结构兼容。依赖未支持能力的字段恒为固定值（如 `store: false`、`previous_response_id: null`、`parallel_tool_calls: true`）。

Token 用量在 `usage` 中返回：

- `input_tokens`：输入 token 数，其中 `input_tokens_details.cached_tokens` 为命中[上下文缓存](kv_cache.md)的 token 数
- `output_tokens`：输出 token 数，其中 `output_tokens_details.reasoning_tokens` 为思维链 token 数

#### 服务端工具用量

服务端网页工具执行成功时，`usage.server_tool_use` 返回整个响应的工具用量：

| 字段 | 含义 |
| --- | --- |
| `tool_search` | 成功的网页搜索查询次数。一次搜索调用包含多个查询时，可能计为多次 |
| `tool_fetch` | 成功的网页读取次数，包括打开网页和在网页内查找文本 |

这些值统计工具操作次数，不是 token 数。`tool_search` 统计网页搜索，不统计 `tool_search_call` 输出项所表示的客户端工具发现操作。失败操作不计入，搜索没有结果时也不增加 `tool_search`。如果两项计数均为零，整个 `server_tool_use` 字段会被省略；字段出现时，两项计数都会返回，包括值为零的项。

`output` 中的 `web_search_call` 项描述单次服务端操作，`usage.server_tool_use` 则提供汇总计数。流式请求应从最终 `response.completed`、`response.incomplete` 或 `response.failed` 事件的 `response.usage` 中读取这些计数；接口不会单独发送工具用量事件，初始响应事件中的 `usage` 为 `null`。

例如，以下请求为 `deepseek-v4-pro` 启用网页搜索。省略 `tool_choice` 时使用默认的自动选择方式：

```json
{
  "model": "deepseek-v4-pro",
  "max_output_tokens": 256,
  "reasoning": {"effort": "none"},
  "tools": [{"type": "web_search"}],
  "input": "Use the web search tool once to search for Python official website. Then reply with only the official site URL."
}
```

以下用量摘录表示成功搜索一次，未读取网页。不同请求的 token 数和工具次数可能不同：

```json
{
  "usage": {
    "input_tokens": 3475,
    "input_tokens_details": {"cached_tokens": 512},
    "output_tokens": 54,
    "output_tokens_details": {"reasoning_tokens": 0},
    "total_tokens": 3529,
    "server_tool_use": {
      "tool_search": 1,
      "tool_fetch": 0
    }
  }
}
```
