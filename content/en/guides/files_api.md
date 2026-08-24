---
title: "Files API"
description: "The Files API lets you upload images and reference them later by file_id. It is the recommended way to:"
source: https://api-docs.deepseek.com/guides/files_api
fetched: 2026-08-23
---

# Files API

The Files API lets you upload images and reference them later by `file_id`. It is the recommended way to:

- Reuse the same image across multiple requests without re-uploading it.
- Send images that would otherwise exceed the 48 MiB request body limit or the 32 MiB per-image inline limit (see [Vision: Limits](vision.md#limits)).

Uploaded files are used together with the `deepseek-v4-flash-vision-exp` model. See [Vision](vision.md) for how to reference an uploaded file in a chat request.

Supported formats: **JPEG, PNG, GIF, and WebP**. The format is detected from the actual file content.

The `base_url` for the examples below is `https://api.deepseek.com`.

---

## Upload a File

Upload a file with a `multipart/form-data` request to `POST /files`. A single file may be at most **64 MiB**, and the upload must complete within **10 minutes**.

Form fields:

| Field | Required | Description |
| --- | --- | --- |
| `file` | Yes | The image file to upload. |
| `purpose` | Yes | Must be `user_data`. |
| `expires_after[anchor]` | No | Must be `created_at` if provided. Required together with `expires_after[seconds]`. |
| `expires_after[seconds]` | No | Lifetime in seconds, between `3600` and `2592000` (1 hour to 30 days). Omit both `expires_after` fields to keep the file permanently. |

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

The response describes the stored file:

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

`expires_at` is only present when you set an expiration at upload time.

---

## List Files

```python
files = client.files.list()
for f in files.data:
    print(f.id, f.filename)
```

```bash
curl https://api.deepseek.com/files \
  -H "Authorization: Bearer <DeepSeek API Key>"
```

Query parameters:

| Parameter | Description |
| --- | --- |
| `after` | A `file_id` cursor for pagination; returns files after this one. |
| `limit` | Number of files to return, between `1` and `1000`. |
| `order` | Sort order by creation time: `asc` (default) or `desc`. |
| `purpose` | Filter by purpose. Only `user_data` is supported. |

The response is a paginated list:

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

## Retrieve File Info

```python
info = client.files.retrieve("file-api-xxxxxxxxxxxxxxxx")
print(info.filename, info.bytes)
```

```bash
curl https://api.deepseek.com/files/file-api-xxxxxxxxxxxxxxxx \
  -H "Authorization: Bearer <DeepSeek API Key>"
```

---

## Delete a File

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

## Use an Uploaded File in a Chat Request

Reference the returned `file_id` with a `file` content block:

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

Files belong to your API key and can be referenced from either API family. Note that referencing a file from the Anthropic-compatible `/messages` endpoint requires the `anthropic-beta: files-api-2025-04-14` header.

Unlike inline (base64) images, files referenced via `file_id` are not subject to the 32 MiB per-image limit — a `file_id` image may be up to 64 MiB in a request.

A `file` block can also carry an image inline as base64 via `file_data` instead of `file_id` (the two are mutually exclusive). When using `file_data` you may also set `filename`; `filename` is not allowed together with `file_id`.

---

## Anthropic-Compatible Files API

The same file operations are also available through the Anthropic-compatible endpoint, with `base_url` = `https://api.deepseek.com/anthropic`. All requests **require** the header `anthropic-beta: files-api-2025-04-14`.

The endpoints are served under `/anthropic/v1/`: the Anthropic SDK appends `/v1` automatically when you point it at the base URL above, but with a plain HTTP client (e.g., curl) you must write the full path.

The endpoints (`POST /anthropic/v1/files`, `GET /anthropic/v1/files`, `GET /anthropic/v1/files/{file_id}`, `DELETE /anthropic/v1/files/{file_id}`) follow the Anthropic Files API shape, which differs from the OpenAI-compatible version above:

|  | OpenAI-compatible | Anthropic-compatible |
| --- | --- | --- |
| List pagination | `after` | `after_id` / `before_id` (mutually exclusive) |
| List `limit` | 1–1000, default 1000 | 1–1000, default 20 |
| List `order` / `purpose` | Supported | Not supported |
| List top-level `object` | `"list"` | Omitted |
| File object size field | `bytes` | `size_bytes` |
| File object type field | `object` | `type` |
| `created_at` | Unix timestamp (seconds) | RFC 3339 string |
| Required header | None | `anthropic-beta: files-api-2025-04-14` |

A file object returned by the Anthropic-compatible endpoint looks like:

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

List files with `after_id` / `before_id` cursors:

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

Deleting a file returns `{ "id": "...", "type": "file_deleted" }`.

---

## Limits

| Limit | Value |
| --- | --- |
| Supported formats | JPEG, PNG, GIF, WebP |
| Max upload file size | 64 MiB |
| Max filename length | 512 characters |
| Max storage per user | 25 GiB |
| Max number of stored files per user | 10000 |
| File expiration range | 1 hour to 30 days, or permanent (omit `expires_after`) |
