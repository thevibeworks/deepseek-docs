---
title: "列出文件"
description: "返回属于该用户的文件列表，使用游标分页。"
source: https://api-docs.deepseek.com/zh-cn/api/list-files
fetched: 2026-08-23
---

# 列出文件

```
GET /files
```

返回属于该用户的文件列表，使用游标分页。

## Request

**Query Parameters**

**after** string

用于分页的 `file_id` 游标，返回排在该文件之后的文件。

**limit** integer

**Possible values:** `>= 1` and `<= 1000`

**Default value:** `1000`

要返回的文件数量，取值在 1 到 1000 之间。

**order** string

**Possible values:** [`asc`, `desc`]

**Default value:** `asc`

按创建时间排序：`asc` 升序，`desc` 降序。

**purpose** string

**Possible values:** [`user_data`]

只返回指定用途的文件，仅支持 `user_data`。

## Responses

- 200

OK, 返回 `file object` 列表。

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**object** stringrequired

**Possible values:** [`list`]

对象的类型，其值为 `list`。

**dataobject[]required**

文件对象列表。

- Array [

**id** stringrequired

文件标识符，形如 `file-api-...`，可在对话补全请求中引用。

**object** stringrequired

**Possible values:** [`file`]

对象的类型，其值为 `file`。

**bytes** integerrequired

文件大小（字节）。

**created\_at** integerrequired

文件创建时的 Unix 时间戳（以秒为单位）。

**filename** stringrequired

文件名。

**purpose** stringrequired

**Possible values:** [`user_data`]

文件的用途。

**expires\_at** integer

文件过期时的 Unix 时间戳（以秒为单位）。仅在上传时设置了过期时间才会出现。

- ]

**first\_id** string

列表中第一个文件的 ID，可用作分页游标。

**last\_id** string

列表中最后一个文件的 ID，可用作分页游标。

**has\_more** booleanrequired

是否还有更多文件。

**[Example (from schema)]**

```json
{
  "object": "list",
  "data": [
    {
      "id": "string",
      "object": "file",
      "bytes": 0,
      "created_at": 0,
      "filename": "string",
      "purpose": "user_data",
      "expires_at": 0
    }
  ],
  "first_id": "string",
  "last_id": "string",
  "has_more": true
}
```

**[Example]**

```json
{
  "object": "list",
  "data": [
    {
      "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9",
      "object": "file",
      "bytes": 102400,
      "created_at": 1700000000,
      "filename": "image.jpg",
      "purpose": "user_data"
    }
  ],
  "first_id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9",
  "last_id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9",
  "has_more": false
}
```

Loading...
