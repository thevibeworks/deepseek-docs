---
title: "Conversation Title"
description: "Set \"title\" true} to have the response carry a short title for the conversation, for example to show in a conversation list. The model writes the title together with the answer, so no extra request is needed."
source: https://api-docs.deepseek.com/guides/conversation_title
fetched: 2026-11-14
---

# Conversation Title

Set `"title": {"enabled": true}` to have the response carry a short title for the conversation, for example to show in a conversation list. The model writes the title together with the answer, so no extra request is needed.

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
    "messages": [{"role": "user", "content": "Will it rain in Beijing tomorrow?"}],
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
    "input": "Will it rain in Beijing tomorrow?",
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
    "messages": [{"role": "user", "content": "Will it rain in Beijing tomorrow?"}],
    "stream": true
  }'
```

Where the title appears in the response:

| Protocol | Non-streaming | Streaming |
| --- | --- | --- |
| Messages | Top-level `title` | `delta.title` of the `message_delta` event |
| Responses | Top-level `title` | `response.title` of the final event |
| Chat Completions | `message.title` | `delta.title` of the last chunk |

```text
event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null,"title":"Beijing weather tomorrow"},"usage":{...}}
```

- After the answer ends, the response waits up to 5 seconds for the title before it finishes. Enable `title` only on the first request of a conversation, and stop enabling it once you have a title.
- A response may come without a title, for example after a refusal or an error. Fall back to something like the first characters of the user's message.
- The title is not billed.
