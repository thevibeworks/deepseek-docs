---
title: "会话标题"
description: "传入 \"title\" true}，响应会带上一个简短的会话标题，可用于对话列表等处展示。标题由模型在回答时顺带生成，无需额外请求。"
source: https://api-docs.deepseek.com/zh-cn/guides/conversation_title
fetched: 2026-11-14
---

# 会话标题

传入 `"title": {"enabled": true}`，响应会带上一个简短的会话标题，可用于对话列表等处展示。标题由模型在回答时顺带生成，无需额外请求。

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search", "name": "deepseek_web_search"},
      {"type": "deepseek_read_url", "name": "deepseek_read_url"}
    ],
    "title": {"enabled": true},
    "messages": [{"role": "user", "content": "北京明天会下雨吗"}],
    "stream": true
  }'
```

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "title": {"enabled": true},
    "input": "北京明天会下雨吗",
    "stream": true
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "title": {"enabled": true},
    "messages": [{"role": "user", "content": "北京明天会下雨吗"}],
    "stream": true
  }'
```

标题在响应中的位置：

| 协议 | 非流式 | 流式 |
| --- | --- | --- |
| Messages | 顶层的 `title` | `message_delta` 事件的 `delta.title` |
| Responses | 顶层的 `title` | 结束事件的 `response.title` |
| Chat Completions | `message.title` | 最后一个 chunk 的 `delta.title` |

```text
event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null,"title":"北京明天天气"},"usage":{...}}
```

- 回答结束后，响应最多等待标题 5 秒才结束。建议只在会话的第一次请求上开启，拿到标题后不再开启。
- 响应不一定带标题，例如被拒答或出错时。请自行兜底，例如取用户消息的前若干个字符。
- 标题不计费。
