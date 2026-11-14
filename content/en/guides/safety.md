---
title: "Model Content Safety"
description: "Set safety_check to {\"level\": \"high\"} to turn on basic risk control, which reviews the model input and output."
source: https://api-docs.deepseek.com/guides/safety
fetched: 2026-11-14
---

# Model Content Safety

Set `safety_check` to `{"level": "high"}` to turn on basic risk control, which reviews the model input and output.

The safety check parameter helps you meet compliance requirements, but it does not replace your obligations as a service provider, such as content safety review. You bear the primary responsibility for content safety review.

Available in the Messages API, the Responses API and the Chat Completions API.

---

## Enable Safety Review

```json
{
  "safety_check": {"level": "high"}
}
```

A complete request in each protocol:

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "safety_check": {"level": "high"},
    "messages": [{"role": "user", "content": "Hello"}]
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
    "input": "Hello"
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
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

| `level` | Review |
| --- | --- |
| `high` | Basic risk control, described on this page |
| `low` | The default content checks of the API, the same as omitting `safety_check` |

- `level` must be `low` or `high`; otherwise the request returns `400`.
- The rest of this page describes `safety_check` set to `high`.
- Works with or without the [web tools](web_tools.md). Without them, the model does not go online, and `tool_choice` must be `auto` or `none`; otherwise the request returns `400`.

---

## What Is Reviewed

Both the input and the output are reviewed. The input includes the user messages, `tool_result` content and so on. When the review does not pass, the request returns `400 Content Exists Risk`, or the response ends with a refusal; see [Handle Refusals](#handling-refusals).

---

## Handle Refusals

With `safety_check` enabled, the connection does not close as soon as the model finishes its output: the service then reviews the complete output, keeping the connection open meanwhile, and the response may still end with a refusal. Handle refusals in your client so that what it displays stays safe.

A refused response ends differently in each protocol:

**[Messages]**

```json
{
  "stop_reason": "refusal",
  "stop_details": {"type": "refusal", "category": null, "explanation": null}
}
```

- Streaming: if no `text` block was sent before the refusal, an empty `text` block is sent before `message_delta`, so SDK helpers that read the final text do not fail.
- Non-streaming: thinking and answer text are removed. `content` keeps the executed tool blocks and one empty `text` block.

**[Responses]**

```json
{
  "status": "incomplete",
  "incomplete_details": {"reason": "content_filter"},
  "output": []
}
```

`status` is `incomplete` with `incomplete_details.reason` set to `content_filter`. `output` keeps only the executed `web_search_call` items. See [Responses API](web_tools.md#responses-api).

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

`finish_reason` is `content_filter`. `content` is an empty string and `annotations` is omitted; `server_tool_calls` is kept, with the thinking of each step cleared. See [Chat Completions API](web_tools.md#chat-completions-api).

If an image in the request does not pass the review, the response also ends with a refusal that names the blocked images, for example `The following images were blocked by content moderation: messages.1.content.0`. This explanation is in `stop_details.explanation` in the Messages API, in the `refusal` content of a `message` item in `output` in the Responses API, and in `message.refusal` in the Chat Completions API (in the `delta.refusal` of the last chunk when streaming).

In all three protocols:

- Text that has already been streamed cannot be withdrawn. When a response ends with a refusal, remove the displayed answer and show your refusal message.
- The response does not give the specific reason for the refusal.
- A request that declares the web tools without `safety_check` can also end with a refusal.
- Tokens consumed before the refusal are billed.

---

## Billing

- The tokens of the safety review are billed as output tokens. They are included in the output tokens in `usage` and reported separately as `safety_tokens`: `usage.output_tokens_details.safety_tokens` in Messages and Responses, and `usage.completion_tokens_details.safety_tokens` in Chat Completions.
- When the input does not pass the review and the request returns `400`, the input tokens are still billed, at the cache hit price.

---

## Compliance Requirements

- With the safety check parameter enabled, we provide basic risk control: the model input and output are reviewed, and a refusal is returned when a risk is detected. If you provide a service to the public, enable this parameter, and fulfill on your own the obligations of a service provider, such as content safety review, large model registration and AI labeling.
- Please comply with our Open Platform Terms of Service: [DeepSeek Open Platform Terms of Service](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html).
