---
title: "Files API"
description: "Files API 让你上传图片，之后通过 file_id 引用。推荐在以下场景使用："
source: https://api-docs.deepseek.com/zh-cn/guides/files_api
fetched: 2026-08-23
---

# Files API

Files API 让你上传图片，之后通过 `file_id` 引用。推荐在以下场景使用：

- 在多个请求中复用同一张图片，无需重复上传。
- 发送会超过 48 MiB 请求体限制或 32 MiB 单图内联限制的图片（见 [图像理解：限制](vision.md#limits)）。

上传的文件与 `deepseek-v4-flash-vision-exp` 模型配合使用。如何在对话请求中引用已上传的文件，请参考 [图像理解](vision.md)。

支持的格式：**JPEG、PNG、GIF、WebP**。格式由文件实际内容判断。

以下示例的 `base_url` 为 `https://api.deepseek.com`。

---

## 上传文件

通过 `multipart/form-data` 请求向 `POST /files` 上传文件。单个文件最大 **64 MiB**，上传需在 **10 分钟**内完成。

表单字段：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| `file` | 是 | 要上传的图片文件。 |
| `purpose` | 是 | 必须为 `user_data`。 |
| `expires_after[anchor]` | 否 | 若提供，必须为 `created_at`。需与 `expires_after[seconds]` 一起使用。 |
| `expires_after[seconds]` | 否 | 有效期（秒），取值在 `3600` 到 `2592000` 之间（1 小时到 30 天）。不传这两个 `expires_after` 字段则文件永久有效。 |

```python
from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

with open("image.jpg", "rb") as f:
    uploaded = client.files.create(file=f, purpose="user_data")

print(uploaded.id)  # file-api-xxxxxxxxxxxxxxxx
```

```bash
curl https://api.deepseek.com/files \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -F purpose="user_data" \
  -F file="@image.jpg"
```

响应描述了已存储的文件：

```json
{
  "id": "file-api-xxxxxxxxxxxxxxxx",
  "object": "file",
  "bytes": 102400,
  "created_at": 1700000000,
  "filename": "image.jpg",
  "purpose": "user_data",
  "expires_at": 1700003600
}
```

只有在上传时设置了有效期，`expires_at` 才会出现。

---

## 列出文件

```python
files = client.files.list()
for f in files.data:
    print(f.id, f.filename)
```

```bash
curl https://api.deepseek.com/files \
  -H "Authorization: Bearer <DeepSeek API Key>"
```

查询参数：

| 参数 | 说明 |
| --- | --- |
| `after` | 用于分页的 `file_id` 游标；返回此文件之后的文件。 |
| `limit` | 返回的文件数量，取值在 `1` 到 `1000` 之间。 |
| `order` | 按创建时间排序：`asc`（默认）或 `desc`。 |
| `purpose` | 按用途过滤。仅支持 `user_data`。 |

响应为分页列表：

```json
{
  "object": "list",
  "data": [
    {
      "id": "file-api-xxxxxxxxxxxxxxxx",
      "object": "file",
      "bytes": 102400,
      "created_at": 1700000000,
      "filename": "image.jpg",
      "purpose": "user_data"
    }
  ],
  "first_id": "file-api-xxxxxxxxxxxxxxxx",
  "last_id": "file-api-xxxxxxxxxxxxxxxx",
  "has_more": false
}
```

---

## 查询文件信息

```python
info = client.files.retrieve("file-api-xxxxxxxxxxxxxxxx")
print(info.filename, info.bytes)
```

```bash
curl https://api.deepseek.com/files/file-api-xxxxxxxxxxxxxxxx \
  -H "Authorization: Bearer <DeepSeek API Key>"
```

---

## 删除文件

```python
client.files.delete("file-api-xxxxxxxxxxxxxxxx")
```

```bash
curl -X DELETE https://api.deepseek.com/files/file-api-xxxxxxxxxxxxxxxx \
  -H "Authorization: Bearer <DeepSeek API Key>"
```

```json
{
  "id": "file-api-xxxxxxxxxxxxxxxx",
  "object": "file",
  "deleted": true
}
```

---

## 在对话请求中使用已上传的文件

使用 `file` 内容块引用返回的 `file_id`：

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

文件归属于你的 API key，可被任一 API 家族引用。注意：通过 Anthropic 兼容 `/messages` 端点引用文件时需携带 `anthropic-beta: files-api-2025-04-14` 请求头。

与内联（base64）图片不同，通过 `file_id` 引用的文件不受 32 MiB 单图限制，请求中单张最大 64 MiB。

`file` 块也可以通过 `file_data` 以 base64 形式内联携带图片，替代 `file_id`（二者互斥）。使用 `file_data` 时还可设置 `filename`；`filename` 不能与 `file_id` 同时出现。

---

## Anthropic 兼容 Files API

同样的文件操作也可通过 Anthropic 兼容端点使用，`base_url` 为 `https://api.deepseek.com/anthropic`。所有请求**必须**带请求头 `anthropic-beta: files-api-2025-04-14`。

端点位于 `/anthropic/v1/` 路径下：Anthropic SDK 设置上述 base URL 时会自动补上 `/v1`；直接用 curl 等裸 HTTP 客户端时需要写完整路径。

这些端点（`POST /anthropic/v1/files`、`GET /anthropic/v1/files`、`GET /anthropic/v1/files/{file_id}`、`DELETE /anthropic/v1/files/{file_id}`）遵循 Anthropic Files API 的形态，与上文 OpenAI 兼容版本存在差异：

|  | OpenAI 兼容 | Anthropic 兼容 |
| --- | --- | --- |
| 列表分页 | `after` | `after_id` / `before_id`（互斥） |
| 列表 `limit` | 1–1000，默认 1000 | 1–1000，默认 20 |
| 列表 `order` / `purpose` | 支持 | 不支持 |
| 列表顶层 `object` | `"list"` | 无 |
| 文件对象大小字段 | `bytes` | `size_bytes` |
| 文件对象类型字段 | `object` | `type` |
| `created_at` | Unix 时间戳（秒） | RFC 3339 字符串 |
| 必需请求头 | 无 | `anthropic-beta: files-api-2025-04-14` |

Anthropic 兼容端点返回的文件对象形如：

```json
{
  "id": "file-api-xxxxxxxxxxxxxxxx",
  "type": "file",
  "size_bytes": 102400,
  "created_at": "2026-01-01T00:00:00+00:00",
  "filename": "image.jpg",
  "mime_type": "image/jpeg"
}
```

使用 `after_id` / `before_id` 游标列出文件：

```bash
curl "https://api.deepseek.com/anthropic/v1/files?limit=20" \
  -H "x-api-key: <DeepSeek API Key>" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```json
{
  "data": [
    {
      "id": "file-api-xxxxxxxxxxxxxxxx",
      "type": "file",
      "size_bytes": 102400,
      "created_at": "2026-01-01T00:00:00+00:00",
      "filename": "image.jpg",
      "mime_type": "image/jpeg"
    }
  ],
  "first_id": "file-api-xxxxxxxxxxxxxxxx",
  "last_id": "file-api-xxxxxxxxxxxxxxxx",
  "has_more": false
}
```

删除文件返回 `{ "id": "...", "type": "file_deleted" }`。

---

## 限制

| 限制项 | 数值 |
| --- | --- |
| 支持的格式 | JPEG、PNG、GIF、WebP |
| 单个上传文件最大大小 | 64 MiB |
| 文件名最大长度 | 512 个字符 |
| 单用户最大存储空间 | 25 GiB |
| 单用户最大存储文件数 | 10000 |
| 文件有效期范围 | 1 小时到 30 天，或不传 `expires_after` 永久有效 |
