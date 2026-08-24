---
title: "查询文件"
description: "返回指定文件的信息。"
source: https://api-docs.deepseek.com/zh-cn/api/retrieve-file
fetched: 2026-08-23
---

# 查询文件

```
GET /files/:file_id
```

返回指定文件的信息。

## Request

**Path Parameters**

**file\_id** stringrequired

要查询的文件 ID。

## Responses

- 200

OK, 返回 `file object`。

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

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

**[Example (from schema)]**

```json
{
  "id": "string",
  "object": "file",
  "bytes": 0,
  "created_at": 0,
  "filename": "string",
  "purpose": "user_data",
  "expires_at": 0
}
```

**[Example]**

```json
{
  "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9",
  "object": "file",
  "bytes": 102400,
  "created_at": 1700000000,
  "filename": "image.jpg",
  "purpose": "user_data"
}
```

Loading...
