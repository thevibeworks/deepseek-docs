---
title: "Build a Chatbot"
description: "The DeepSeek API offers the same conversation features as DeepSeek Chat on the web and in the app: web search, deep thinking search, file input and URL reading, plus basic risk control for model content safety. You can use them to build your own chatbot."
source: https://api-docs.deepseek.com/guides/build_a_chatbot
fetched: 2026-11-14
---

# Build a Chatbot

The DeepSeek API offers the same conversation features as DeepSeek Chat on the web and in the app: web search, deep thinking search, file input and URL reading, plus basic risk control for model content safety. You can use them to build your own chatbot.

The service runs the searches and URL reading. Your client only shows the returned blocks and passes them back unchanged in the next round.

---

## Feature Map

| Chatbot feature | Description | Guide |
| --- | --- | --- |
| Web search | With thinking disabled and the `deepseek_web_search` tool enabled, the model runs web or image searches as the question requires and answers with citations | [Web Search](web_tools.md#web-search) |
| Deep thinking search | With thinking enabled and the `deepseek_web_search` tool enabled, the model searches the web and reads links on its own over multiple reasoning steps | [Deep Thinking Search](web_tools.md#search-while-thinking) |
| File input | Upload files such as PDF, Word, PowerPoint and image files; after plain-text extraction or rich-layout parsing, they are added to the conversation context for the model to answer from | [File Parsing](document_parsing.md) |
| URL reading | With the `deepseek_read_url` tool enabled, the model detects links in the user message, fetches the pages and answers with them in context | [URL Reading](web_tools.md#read-links) |
| Model content safety | With the safety check parameter enabled, we provide basic risk control: the model input and output are reviewed, and a refusal marker is returned when a risk is found. If you provide a service to the public, enable this parameter and fulfill obligations such as content safety review, large model registration and AI labeling | [Model Content Safety](safety.md) |
| User metadata marker | Tell the model the current date and the user's location and language, so that answers fit the user's situation | [User Metadata Marker](latest_reminder.md) |
| Conversation title | Generates a short title from the conversation when the answer ends | [Conversation Title](conversation_title.md) |
| Read aloud | Turns the model's answer into speech | [Text to Speech](tts.md) |
| Voice input | Transcribes the user's speech into text to send as a message | [Speech to Text](asr.md) |

---

## Demo

DeepSeek provides an open-source demo chat client that shows how to build a chatbot with these APIs. Enter your API key to start. You can also import the chat history you exported from DeepSeek Chat and continue your conversations.

- Try the demo: <https://cdn.deepseek.com/chat-demo>
- Source code: <https://github.com/deepseek-ai/chat-demo>

Your API key, conversations and uploaded images are stored only in your browser. The demo is for demonstration only.

The demo shows:

- Web search, deep thinking search and URL reading
- Uploading images and documents
- Model content safety, including image review
- Conversation titles, and renaming and deleting conversations
- Editing a message, regenerating, and continuing a reply
- Reading answers aloud, and voice input
- Choosing a language and location in the settings, which are passed to the model as the user metadata marker
- Importing and exporting chat history (an import replaces the existing history)
- Markdown rendering, including Mermaid diagrams
- A Chinese and English interface, with light and dark themes

---

## Choose a Protocol

The chat features are available in the Messages API, the Responses API and the Chat Completions API.

| Protocol | Endpoint |
| --- | --- |
| Messages | `POST https://api.deepseek.com/anthropic/v1/messages` |
| Responses | `POST https://api.deepseek.com/responses` |
| Chat Completions | `POST https://api.deepseek.com/chat/completions` |

Use the `deepseek-flash` model.

---

## Quick Example

A streaming request with the web tools, safety review and the conversation title enabled:

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "thinking": {"type": "enabled"},
    "tools": [
      {"type": "deepseek_web_search", "name": "deepseek_web_search"},
      {"type": "deepseek_read_url", "name": "deepseek_read_url"}
    ],
    "safety_check": {"level": "high"},
    "title": {"enabled": true},
    "messages": [{"role": "user", "content": "What is new in DeepSeek V4.1?"}],
    "stream": true
  }'
```

The stream of this request, shortened:

```text
event: message_start
data: {"type":"message_start","message":{"id":"b161a9be-...","type":"message","role":"assistant","model":"deepseek-flash","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":40,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":0,"service_tier":"standard"}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"thinking","thinking":"","signature":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"thinking_delta","thinking":"..."}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"signature_delta","signature":"b161a9be-..."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"server_tool_use","id":"srvtoolu_ds_00_b2baebaf...","name":"deepseek_web_search","input":{"action":"search","queries":["DeepSeek V4.1 new features","DeepSeek V4.1 release notes"]},"caller":{"type":"direct"},"kind":"deep_search"}}

event: content_block_stop
data: {"type":"content_block_stop","index":1}

event: content_block_start
data: {"type":"content_block_start","index":2,"content_block":{"type":"web_search_tool_result","tool_use_id":"srvtoolu_ds_00_b2baebaf...","content":[{"type":"web_search_result","title":"...","url":"https://api-docs.deepseek.com/news/news261017/","encrypted_content":"...","page_age":"2026-10-16T16:00:00+00:00","snippet":"...","site_name":"DeepSeek","site_icon":"https://cdn.deepseek.com/site-icons/deepseek.com"}],"kind":"deep_search"}}

...

event: content_block_start
data: {"type":"content_block_start","index":15,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":15,"delta":{"type":"text_delta","text":"Deep"}}

event: content_block_delta
data: {"type":"content_block_delta","index":15,"delta":{"type":"citations_delta","citation":{"type":"web_search_result_location","url":"https://api-docs.deepseek.com/news/news261017/","title":"...","encrypted_index":"","cited_text":"..."}}}

...

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null,"title":"..."},"usage":{"input_tokens":9078,"cache_creation_input_tokens":0,"cache_read_input_tokens":4096,"output_tokens":1686,"service_tier":"standard","server_tool_use":{"web_search_requests":1,"web_fetch_requests":0,"tool_search":2,"tool_fetch":0,"tool_image_search":0}}}

event: message_stop
data: {"type":"message_stop"}
```

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "reasoning": {"effort": "high"},
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "safety_check": {"level": "high"},
    "title": {"enabled": true},
    "input": "What is new in DeepSeek V4.1?",
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
    "thinking": {"type": "enabled"},
    "tools": [
      {"type": "deepseek_web_search"},
      {"type": "deepseek_read_url"}
    ],
    "safety_check": {"level": "high"},
    "title": {"enabled": true},
    "messages": [{"role": "user", "content": "What is new in DeepSeek V4.1?"}],
    "stream": true
  }'
```

---

## Render a Response

A chatbot response contains several kinds of content blocks. The screenshot below marks where each block appears in DeepSeek Chat.

![A DeepSeek Chat conversation with the thinking, search, page reading and answer blocks marked](https://api-docs.deepseek.com/img/chatbot_response_blocks_en.webp)

| Block | What to show |
| --- | --- |
| `thinking` | The collapsible thinking panel |
| `server_tool_use` + `web_search_tool_result` | A search step with result cards (title, site name, icon) |
| `server_tool_use` + `web_fetch_tool_result` | A page that was opened or a link that was read |
| `text` with `citations` | The answer, with citation markers that link to the sources |
| `stop_reason: "refusal"` | Replace the answer with your refusal message |

See [Web Tools](web_tools.md#response-blocks) and [Model Content Safety](safety.md#handling-refusals) for the block formats.

---

## Ignored Parameters

When a request declares `deepseek_web_search` or `deepseek_read_url`, sets `safety_check` to `high`, or enables `title`, the service decides the following parameters, and the values in the request are ignored:

| Protocol | Ignored parameters |
| --- | --- |
| Messages | `temperature`, `top_p`, `top_k`, `stop_sequences`, `thinking.budget_tokens`, `preserve_thinking`, `tool_choice.disable_parallel_tool_use`, `metadata` (except `user_id`) |
| Responses | `temperature`, `top_p`, `reasoning.summary`, `text.verbosity`, `include`, `max_tool_calls`, `truncation`, `metadata`, `parallel_tool_calls`, `store` |
| Chat Completions | `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`, `stop`, `seed`, `n`, `preserve_thinking`, `parallel_tool_calls` |

`max_tokens` (`max_output_tokens` in the Responses API) works as usual. It limits the output of each inference step in a round, not the total output of the round.

---

## Compliance Requirements

- With the safety check parameter enabled, we provide basic risk control: the model input and output are reviewed, and a refusal is returned when a risk is detected. If you provide a service to the public, enable this parameter, and fulfill on your own the obligations of a service provider, such as content safety review, large model registration and AI labeling.
- Please comply with our Open Platform Terms of Service: [DeepSeek Open Platform Terms of Service](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html).
