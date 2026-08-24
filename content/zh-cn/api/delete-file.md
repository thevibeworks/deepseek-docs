---
title: "删除文件"
description: "删除一个文件。"
source: https://api-docs.deepseek.com/zh-cn/api/delete-file
fetched: 2026-08-23
---

# 删除文件

```
DELETE /files/:file_id
```

删除一个文件。

## Request

**Path Parameters**

**file\_id** stringrequired

要删除的文件 ID。

## Responses

- 200

OK, 返回删除状态。

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**id** stringrequired

被删除文件的 ID。

**object** stringrequired

**Possible values:** [`file`]

对象的类型，其值为 `file`。

**deleted** booleanrequired

文件是否被成功删除。

**[Example (from schema)]**

```json
{
  "id": "string",
  "object": "file",
  "deleted": true
}
```

**[Example]**

```json
{
  "id": "file-api-0a1b2c3d4e5f60718293a4b5c6d7e8f9",
  "object": "file",
  "deleted": true
}
```

Loading...
