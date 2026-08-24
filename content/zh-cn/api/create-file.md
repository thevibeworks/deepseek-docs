---
title: "上传文件"
description: "上传图片文件，之后可在对话补全请求中通过其 `file_id` 引用。"
source: https://api-docs.deepseek.com/zh-cn/api/create-file
fetched: 2026-08-23
---

# 上传文件

```
POST /files
```

上传图片文件，之后可在对话补全请求中通过其 `file_id` 引用。

支持的格式：JPEG、PNG、GIF、WebP。格式由文件内容判断。详见 [Files API 指南](../guides/files_api.md)。

## Request

**[multipart/form-data]**

**Bodyrequired**

**file** binaryrequired

要上传的图片文件。支持的格式：JPEG、PNG、GIF、WebP。单个文件最大 64 MiB。

**purpose** stringrequired

**Possible values:** [`user_data`]

上传文件的用途，必须为 `user_data`。

**expires\_after[anchor]** string

**Possible values:** [`created_at`]

过期时间的锚点。若提供，必须为 `created_at`，且需与 `expires_after[seconds]` 一起使用。

**expires\_after[seconds]** integer

**Possible values:** `>= 3600` and `<= 2592000`

文件的有效期（秒），取值在 3600（1 小时）到 2592000（30 天）之间。需与 `expires_after[anchor]` 一起使用。不传这两个 `expires_after` 字段则文件永久有效。

## Responses

- 200

OK, 返回上传的 `file object`。

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
