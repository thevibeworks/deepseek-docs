---
title: "Lists Models"
description: "Lists the currently available models, and provides metadata about each one, such as its display name, context window, output limit, supported input/output modalities, supported effort levels, and per-protocol API capabilities. Check [Models & Pricing](/quick_start/pricing) for our currently supported models."
source: https://api-docs.deepseek.com/api/list-models/
fetched: 2026-11-28
---

# Lists Models

```
GET /models
```

Lists the currently available models, and provides metadata about each one, such as its display name, context window, output limit, supported input/output modalities, supported effort levels, and per-protocol API capabilities. Check [Models & Pricing](../quick_start/pricing.md) for our currently supported models.

## Responses

- 200

OK, returns A list of models

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**object** stringrequired

**Possible values:** `list`

The object type, which is always `list`.

**data**

object[]

required

The list of model objects.

Describes a DeepSeek model offering that can be used with the API. Besides the identifier fields, each model carries machine-readable metadata about its capabilities and limits; a metadata field may be omitted when the information is not available for that model.

- Array [

**id** stringrequired

The model identifier, which can be referenced in the API endpoints.

**object** stringrequired

**Possible values:** `model`

The object type, which is always "model".

**owned\_by** stringrequired

The organization that owns the model.

**name** string

The display name of the model, for use in model pickers and model discovery tools.

**context\_window** integer

The total token capacity of the context window, counting both input and output tokens.

**max\_output\_tokens** integer

The maximum number of output tokens the server allows in a single response, i.e. the maximum accepted value of `max_tokens`.

**input\_modalities** string[]

**Possible values:** `text`, `image`

The input types the model accepts.

**output\_modalities** string[]

**Possible values:** `text`

The media types the model can generate.

**effort**

object

The effort levels available when thinking mode is enabled.

**supported\_levels** string[]required

The effort levels the model supports when thinking mode is enabled, in the recommended display order. These are the values accepted by the `reasoning_effort` parameter; `none`, which turns thinking mode off, is not included.

**default\_level** string

The effort level the server uses when thinking mode is enabled and the request does not specify one. Always one of `supported_levels`. Only present when the server defines a default for the model.

**api\_capabilities**

object

Model behavior declared per API protocol.

**anthropic\_messages**

object

Capabilities that apply when the model is used through the [Anthropic Messages API](../guides/anthropic_api.md).

**system\_prompt\_update** stringrequired

**Possible values:** `leading-only`, `in-history`

How the model picks up an updated system prompt during a conversation.

- `leading-only`: only the system prompt at the start of the conversation takes effect. To change the system prompt, modify that leading system prompt; system messages appearing later in the history are not treated as system prompt updates.
- `in-history`: a `system` message may be appended to the conversation history. The latest `system` message updates the effective system prompt; when instructions conflict, later `system` messages take precedence over earlier ones (earlier messages remain in the history, and non-conflicting instructions can still apply).

**tool\_update** stringrequired

**Possible values:** `leading-only`, `addition-only`

How the model handles tool changes during a conversation.

- `leading-only`: only the tools declared at the top level of the request are used. `defer_loading`, `tool_addition`, and `tool_reference` loading effects are ignored (`tool_reference` is rendered as plain text). When the available tools change, resend the complete `tools` array in every request.
- `addition-only`: tools declared with `defer_loading: true` are loaded when a later `system` message contains a `tool_addition` block, or when a `tool_result` contains a `tool_reference` block. `tool_removal` blocks are not supported.

- ]

**[Example]**

```json
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-flash",
      "object": "model",
      "owned_by": "deepseek",
      "name": "DeepSeek-V4.1-Flash",
      "context_window": 1048576,
      "max_output_tokens": 393216,
      "input_modalities": ["text", "image"],
      "output_modalities": ["text"],
      "effort": {
        "supported_levels": ["low", "high", "max"],
        "default_level": "high"
      },
      "api_capabilities": {
        "anthropic_messages": {
          "system_prompt_update": "in-history",
          "tool_update": "addition-only"
        }
      }
    },
    {
      "id": "deepseek-v4-pro",
      "object": "model",
      "owned_by": "deepseek",
      "name": "DeepSeek-V4-Pro",
      "context_window": 1048576,
      "max_output_tokens": 393216,
      "input_modalities": ["text"],
      "output_modalities": ["text"],
      "effort": {
        "supported_levels": ["low", "high", "max"],
        "default_level": "high"
      },
      "api_capabilities": {
        "anthropic_messages": {
          "system_prompt_update": "leading-only",
          "tool_update": "leading-only"
        }
      }
    }
  ]
}
```

Loading...
