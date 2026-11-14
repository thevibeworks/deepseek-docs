---
title: "模型内容安全"
description: "在请求中传入 \"safety_check\" \"high\"}，即可开启基础风控，审核模型的输入与输出。"
source: https://api-docs.deepseek.com/zh-cn/guides/safety
fetched: 2026-11-14
---

# 模型内容安全

在请求中传入 `"safety_check": {"level": "high"}`，即可开启基础风控，审核模型的输入与输出。

该安全校验参数帮助您满足合规要求，但不能替代您作为服务提供者的内容安全审核等义务。您是内容安全审核的第一责任人。

可在 Messages API、Responses API 与 Chat Completions API 中使用。

---

## 开启安全审核

```json
{
  "safety_check": {"level": "high"}
}
```

各协议下完整的请求：

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "input": "你好"
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

| `level` | 审核 |
| --- | --- |
| `high` | 开启基础风控，即本页介绍的内容 |
| `low` | API 默认的内容检查，与不传 `safety_check` 相同 |

- `level` 只能是 `low` 或 `high`，否则返回 `400`。
- 本页其余部分描述的是 `safety_check` 为 `high` 时的行为。
- 可以与 [联网工具](web_tools.md) 一起使用，也可以单独使用。单独使用时不会联网，`tool_choice` 只能为 `auto` 或 `none`，否则返回 `400`。

---

## 审核范围

审核请求的输入和模型的输出。输入包括用户消息、`tool_result` 内容等。未通过审核时，请求返回 `400 Content Exists Risk`，或响应以拒答结束，见 [处理拒答](#handling-refusals)。

---

## 处理拒答

开启 `safety_check` 后，模型输出结束时连接不会立即关闭：服务端还会对完整的输出做一次安全审核，审核期间连接保持打开，之后响应仍可能以拒答结束。请在前端处理拒答，确保内容展示的安全性。

被拒答的响应在各协议中的结束方式不同：

**[Messages]**

```json
{
  "stop_reason": "refusal",
  "stop_details": {"type": "refusal", "category": null, "explanation": null}
}
```

- 流式：如果拒答前还没有下发过 `text` 块，服务端会在 `message_delta` 之前补发一个空的 `text` 块，避免 SDK 读取最终文本的辅助方法报错。
- 非流式：思考和回答文本会被清空，`content` 中保留已执行的工具块和一个空的 `text` 块。

**[Responses]**

```json
{
  "status": "incomplete",
  "incomplete_details": {"reason": "content_filter"},
  "output": []
}
```

`status` 为 `incomplete`，`incomplete_details.reason` 为 `content_filter`。`output` 只保留已执行的 `web_search_call`。见 [Responses API](web_tools.md#responses-api)。

**[Chat Completions]**

```json
{
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": ""},
      "finish_reason": "content_filter"
    }
  ]
}
```

`finish_reason` 为 `content_filter`。`content` 为空字符串，不返回 `annotations`；`server_tool_calls` 保留，各步的思考被清空。见 [Chat Completions API](web_tools.md#chat-completions-api)。

请求中的图片未通过审核时，响应同样以拒答结束，并指出是哪些图片，例如 `The following images were blocked by content moderation: messages.1.content.0`。这段说明在 Messages API 中位于 `stop_details.explanation`，在 Responses API 中位于 `output` 里一个 `message` 的 `refusal` 内容，在 Chat Completions API 中位于 `message.refusal`（流式时为最后一个 chunk 的 `delta.refusal`）。

三个协议的共同点：

- 已经流式下发的文本无法撤回。响应以拒答结束时，请删除已展示的回答，改为展示你的拒答文案。
- 响应不会说明拒答的具体原因。
- 没有开启 `safety_check` 但声明了联网工具的请求，也可能以拒答结束。
- 拒答前已消耗的 Token 照常计费。

---

## 计费

- 安全审核产生的 Token 按输出 Token 计费。它们已包含在 `usage` 的输出 Token 中，并单独列在 `safety_tokens` 里：Messages 与 Responses 为 `usage.output_tokens_details.safety_tokens`，Chat Completions 为 `usage.completion_tokens_details.safety_tokens`。
- 输入未通过审核、请求返回 `400` 时，输入 Token 仍会计费，按缓存命中的价格计算。

---

## 合规要求

- 开启安全校验参数后，我们将提供基础风控，审核模型输入输出，命中风险时返回拒答标识。如您对外提供服务，请开启该参数，并自行履行服务提供者应承担的内容安全审核、大模型登记、AI 标识等义务。
- 请您遵守我们的开放平台服务协议：[DeepSeek 开放平台服务协议](https://cdn.deepseek.com/policies/zh-CN/deepseek-open-platform-terms-of-service.html)。
