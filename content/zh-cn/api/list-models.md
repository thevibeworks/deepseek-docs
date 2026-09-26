---
title: "获取模型列表"
description: "列出当前可用的模型，并提供各模型的元数据：展示名称、上下文窗口、输出上限、支持的输入/输出模态、支持的推理强度（effort）档位，以及按 API 协议声明的能力。请前往[模型 & 价格](/zh-cn/quick_start/pricing)查看当前支持的模型列表"
source: https://api-docs.deepseek.com/zh-cn/api/list-models
fetched: 2026-09-26
---

# 获取模型列表

```
GET /models
```

列出当前可用的模型，并提供各模型的元数据：展示名称、上下文窗口、输出上限、支持的输入/输出模态、支持的推理强度（effort）档位，以及按 API 协议声明的能力。请前往[模型 & 价格](../quick_start/pricing.md)查看当前支持的模型列表

## Responses

- 200

OK, 返回模型列表

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**object** stringrequired

**Possible values:** [`list`]

对象的类型，其值为 `list`。

**data**

object[]

required

模型对象列表。

- Array [

**id** stringrequired

模型的标识符，用于在 API 接口中引用该模型。

**object** stringrequired

**Possible values:** [`model`]

对象的类型，其值为 `model`。

**owned\_by** stringrequired

拥有该模型的组织。

**name** string

模型的展示名称，供模型选择器和模型发现工具使用。

**context\_window** integer

上下文窗口的 token 总容量，输入与输出 token 合计。

**max\_output\_tokens** integer

服务端允许单次响应输出的 token 数的上限，即 `max_tokens` 可接受的最大值。

**input\_modalities** string[]

**Possible values:** [`text`, `image`]

模型接受的输入类型。

**output\_modalities** string[]

**Possible values:** [`text`]

模型可生成的媒体类型。

**effort**

object

开启思考模式时可用的推理强度（effort）档位。

**supported\_levels** string[]required

开启思考模式时模型支持的推理强度档位，按建议的展示顺序排列。这些值即 `reasoning_effort` 参数可接受的取值；用于关闭思考模式的 `none` 不包含在内。

**default\_level** string

开启思考模式且请求未指定推理强度时，服务端使用的默认档位。一定属于 `supported_levels`。仅在服务端为该模型定义了默认档位时返回。

**api\_capabilities**

object

按 API 协议声明的模型行为。

**anthropic\_messages**

object

通过 [Anthropic Messages API](../guides/anthropic_api.md) 使用该模型时适用的能力。

**system\_prompt\_update** stringrequired

**Possible values:** [`leading-only`, `in-history`]

对话过程中更新 system 提示词时，模型采用新提示词的方式。

- `leading-only`：只有对话开头的 system 提示词生效。要更改提示词，需修改开头这条 system 提示词；历史中后续出现的 system 消息不会被视为提示词更新。
- `in-history`：可以在对话历史中追加 `system` 消息。历史中最新的一条 `system` 消息提供完整的有效提示词，并替代此前的所有 system 提示词。

- ]

**[Example (from schema)]**

```json
{
  "object": "list",
  "data": [
    {
      "id": "string",
      "object": "model",
      "owned_by": "string",
      "name": "string",
      "context_window": 0,
      "max_output_tokens": 0,
      "input_modalities": [
        "text"
      ],
      "output_modalities": [
        "text"
      ],
      "effort": {
        "supported_levels": [
          "string"
        ],
        "default_level": "string"
      },
      "api_capabilities": {
        "anthropic_messages": {
          "system_prompt_update": "leading-only"
        }
      }
    }
  ]
}
```

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
          "system_prompt_update": "in-history"
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
          "system_prompt_update": "leading-only"
        }
      }
    }
  ]
}
```

Loading...
