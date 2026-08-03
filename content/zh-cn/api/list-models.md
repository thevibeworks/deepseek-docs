---
title: "获取模型列表"
description: "列出可用的模型列表，并提供相关模型的基本信息。请前往[模型 & 价格](/zh-cn/quick_start/pricing)查看当前支持的模型列表"
source: https://api-docs.deepseek.com/zh-cn/api/list-models
fetched: 2026-08-02
---

# 获取模型列表

```
GET /models
```

列出可用的模型列表，并提供相关模型的基本信息。请前往[模型 & 价格](../quick_start/pricing.md)查看当前支持的模型列表

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

**dataModel[]required**

- Array [

**id** stringrequired

模型的标识符

**object** stringrequired

**Possible values:** [`model`]

对象的类型，其值为 `model`。

**owned\_by** stringrequired

拥有该模型的组织。

- ]

**[Example (from schema)]**

```json
{
  "object": "list",
  "data": [
    {
      "id": "string",
      "object": "model",
      "owned_by": "string"
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
      "id": "deepseek-v4-flash",
      "object": "model",
      "owned_by": "deepseek"
    },
    {
      "id": "deepseek-v4-pro",
      "object": "model",
      "owned_by": "deepseek"
    }
  ]
}
```

Loading...
