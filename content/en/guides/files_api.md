---
title: "Files API"
description: "The Files API lets you upload files and reference them later by file_id. You can upload two kinds of files:"
source: https://api-docs.deepseek.com/guides/files_api
fetched: 2026-11-14
---

# Files API

The Files API lets you upload files and reference them later by `file_id`. You can upload two kinds of files:

- **Images**: JPEG, PNG, GIF and WebP. The format is detected from the actual file content. See [Vision](vision.md) for how to reference them.
- **Documents**: PDF, Word, PowerPoint, Excel, ebooks and plain text. See [File Parsing](document_parsing.md) for how to reference them.

Uploaded files are used together with the `deepseek-flash` model.

---

## Upload a File

Upload a file with a `multipart/form-data` request to `POST /files`. The size limit of a file depends on its type: **64 MiB** for images, **100 MiB** for documents such as PDF, Word and PowerPoint files, and **32 MiB** for plain text, spreadsheets and ebooks. The time limit for an upload also depends on the file type: **120 seconds** for documents such as PDF, Word and PowerPoint files, and **10 minutes** for other files.

Form fields:

| Field | Required | Description |
| --- | --- | --- |
| `file` | Yes | The file to upload. The accepted file types depend on `purpose`; see the table below. |
| `purpose` | Yes | What the file is for. See the values below. |
| `expires_after[anchor]` | No | Must be `created_at` if provided. Required together with `expires_after[seconds]`. |
| `expires_after[seconds]` | No | Lifetime in seconds, between `3600` and `2592000` (1 hour to 30 days). Omit both `expires_after` fields to keep the file permanently. |

| `purpose` | File | Use |
| --- | --- | --- |
| `user_data` | Images (JPEG, PNG, GIF, WebP); plain text (txt, md, csv, json, source code files and so on); spreadsheets (XLSX, XLS) and ebooks (EPUB, MOBI) | Reference the image in a chat request; see [Vision](vision.md). For plain text, spreadsheets and ebooks, see [File Parsing](document_parsing.md#text-files) |
| `text_recognition` | PDF, Word (DOC, DOCX), PowerPoint (PPT, PPTX), and images such as PNG, JPEG, WebP, GIF, BMP and TIFF | Only the text is parsed; figures in the document are not given to the model. See [File Parsing](document_parsing.md) |
| `rich_layout_recognition` | Same as above | The text and the figures in the document are given to the model together. See [File Parsing](document_parsing.md) |

For a document, send `purpose` before the `file` field. Uploading a PDF, Word or PowerPoint file with `user_data` returns `400`.

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
| `purpose` | Filter by purpose. `user_data`, `text_recognition` or `rich_layout_recognition`. |

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
    model="deepseek-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
            ],
        },
    ],
)
print(response.choices[0].message.content)
```

Files belong to your account: all API keys under the same account share them, and they can be referenced from either API family. Note that referencing a file from the Anthropic-compatible `/messages` endpoint requires the `anthropic-beta: files-api-2025-04-14` header.

Unlike inline (base64) images, files referenced via `file_id` are not subject to the 32 MiB per-image limit — a `file_id` image may be up to 64 MiB in a request.

A `file` block can also carry an image inline as base64 via `file_data` instead of `file_id` (the two are mutually exclusive). When using `file_data` you may also set `filename`; `filename` is not allowed together with `file_id`.

---

## Documents

To upload documents such as PDF, Word and PowerPoint files, set `purpose` to `text_recognition` or `rich_layout_recognition`. The `purpose` field must come before the `file` field in the form.

- The file is parsed during the upload, and the upload returns the file object only after parsing succeeds, so every `file_id` you get is ready.
- Documents uploaded this way cannot be used as images. To reference a document in a chat request, see [File Parsing](document_parsing.md#document-qa).
- Neither the uploaded original file nor the parsing result can be downloaded.

See [File Parsing](document_parsing.md) for the limits, errors and billing.

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

On the Anthropic-compatible endpoint, the `purpose` field is optional and defaults to `user_data`. To upload documents such as PDF, Word and PowerPoint files, send `purpose` set to `text_recognition` or `rich_layout_recognition` before the `file` field.

---

## Limits

| Limit | Value |
| --- | --- |
| Supported formats | Images: JPEG, PNG, GIF, WebP. For other files, see the `purpose` table above |
| Max upload file size | Images: 64 MiB; documents such as PDF, Word and PowerPoint files: 100 MiB; plain text, spreadsheets and ebooks: 32 MiB |
| Max filename length | 512 bytes |
| Max storage per user | 25 GiB |
| Max number of stored files per user | 10000 |
| File expiration range | 1 hour to 30 days, or permanent (omit `expires_after`) |
