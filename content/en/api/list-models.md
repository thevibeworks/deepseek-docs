---
title: "Lists Models"
description: "Lists the currently available models, and provides basic information about each one such as the owner and availability. Check [Models & Pricing](/quick_start/pricing) for our currently supported models."
source: https://api-docs.deepseek.com/api/list-models
fetched: 2026-08-02
---

# Lists Models

```
GET /models
```

Lists the currently available models, and provides basic information about each one such as the owner and availability. Check [Models & Pricing](../quick_start/pricing.md) for our currently supported models.

## Responses

- 200

OK, returns A list of models

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

The model identifier, which can be referenced in the API endpoints.

**object** stringrequired

**Possible values:** [`model`]

The object type, which is always "model".

**owned\_by** stringrequired

The organization that owns the model.

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
