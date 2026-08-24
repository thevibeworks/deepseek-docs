---
title: "Using the Anthropic API"
description: "To meet the demand for using the Anthropic API ecosystem, our API has added support for the Anthropic API format, with the base_url being https://api.deepseek.com/anthropic."
source: https://api-docs.deepseek.com/guides/anthropic_api
fetched: 2026-08-23
---

# Using the Anthropic API

To meet the demand for using the Anthropic API ecosystem, our API has added support for the Anthropic API format, with the `base_url` being `https://api.deepseek.com/anthropic`.

With simple configuration, you can integrate the capabilities of DeepSeek into the Anthropic API ecosystem.

---

## Use DeepSeek in Claude Code

Please refer to [Integrate with Claude Code](../quick_start/agent_integrations/claude_code.md).

## Invoke DeepSeek Model via Anthropic API

1. Install Anthropic SDK

```text
pip install anthropic
```

2. Config Environment Variables

```text
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

3. Invoke the API

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

**Note:** When you pass an unsupported model name to DeepSeek's Anthropic API, the API backend will automatically map it to the `deepseek-v4-flash` model.

---

## Anthropic Model Mapping

When you use the Anthropic API, we map the Claude model names you pass in:

- Models starting with claude-opus are mapped to deepseek-v4-pro
- Models starting with claude-haiku or claude-sonnet are mapped to deepseek-v4-flash

With this mapping, when using the developer mode of the new Claude Desktop APP, you can bypass the APP's model name restrictions by simply changing the base\_url and api\_key to connect to DeepSeek models.

---

## Anthropic API Compatibility Details

This section lists the compatibility details of the DeepSeek API with the Anthropic API. For the full Anthropic API format definition, please refer to the [official Anthropic API reference](https://platform.claude.com/docs/en/api/python/beta/messages/create).

### HTTP Header

| Field | Support Status |
| --- | --- |
| anthropic-beta | Ignored for `/messages`; required (`files-api-2025-04-14`) for Files API endpoints — see [Files API](files_api.md#anthropic-compatible-files-api) |
| anthropic-version | Ignored |
| x-api-key | Fully Supported |

### Simple Fields

| Field | Support Status |
| --- | --- |
| model | Use DeepSeek Model Instead |
| max\_tokens | Fully Supported |
| container | Ignored |
| mcp\_servers | Ignored |
| metadata | `user_id` is supported, others are ignored Please refer to [Rate Limit & Isolation](../quick_start/rate_limit.md) for more information about `user_id` parameter. |
| service\_tier | Ignored |
| stop\_sequences | Fully Supported |
| stream | Fully Supported |
| system | Fully Supported |
| temperature | Fully Supported (range [0.0 ~ 2.0]) |
| thinking | Supported (`budget_tokens` is ignored) |
| output\_config | Only `effort` is supported |
| top\_k | Ignored |
| top\_p | Fully Supported |

### Tool Fields

#### tools

| Field | Support Status |
| --- | --- |
| name | Fully Supported |
| input\_schema | Fully Supported |
| description | Fully Supported |
| cache\_control | Ignored |

#### tool\_choice

| Value | Support Status |
| --- | --- |
| none | Fully Supported |
| auto | Supported (`disable_parallel_tool_use` is ignored) |
| any | Supported (`disable_parallel_tool_use` is ignored) |
| tool | Supported (`disable_parallel_tool_use` is ignored) |

### Message Fields

| Field | Variant | Sub-Field | Support Status |
| --- | --- | --- | --- |
| content | string |  | Fully Supported |
| array, type="text" | text | Fully Supported |
| cache\_control | Ignored |
| citations | Ignored |
| array, type="image" | source | Supported. `source.type` can be base64 (media types: jpeg, png, gif, webp), url, or file (the file variant requires the header `anthropic-beta: files-api-2025-04-14`) |
| array, type = "document" |  | Not Supported |
| array, type = "search\_result" |  | Not Supported |
| array, type = "thinking" |  | Supported |
| array, type="redacted\_thinking" |  | Not Supported |
| array, type = "tool\_use" | id | Fully Supported |
| input | Fully Supported |
| name | Fully Supported |
| cache\_control | Ignored |
| array, type = "tool\_result" | tool\_use\_id | Fully Supported |
| content | Fully Supported |
| cache\_control | Ignored |
| is\_error | Ignored |
| array, type = "server\_tool\_use" |  | Supported |
| array, type = "web\_search\_tool\_result" |  | Supported |
| array, type = "code\_execution\_tool\_result" |  | Not Supported |
| array, type = "mcp\_tool\_use" |  | Not Supported |
| array, type = "mcp\_tool\_result" |  | Not Supported |
| array, type = "container\_upload" |  | Not Supported |
