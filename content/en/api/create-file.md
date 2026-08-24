---
title: "Upload File"
description: "Upload an image file that can later be referenced by its `file_id` in chat completion requests."
source: https://api-docs.deepseek.com/api/create-file
fetched: 2026-08-23
---

# Upload File

```
POST /files
```

Upload an image file that can later be referenced by its `file_id` in chat completion requests.

Supported formats: JPEG, PNG, GIF, and WebP. The format is detected from the file content. See the [Files API guide](../guides/files_api.md) for details.

## Request

**[multipart/form-data]**

**Bodyrequired**

**file** binaryrequired

The image file to upload. Supported formats: JPEG, PNG, GIF, and WebP. Maximum file size: 64 MiB.

**purpose** stringrequired

**Possible values:** [`user_data`]

The intended purpose of the uploaded file. Must be `user_data`.

**expires\_after[anchor]** string

**Possible values:** [`created_at`]

The anchor for the expiration. Must be `created_at` if provided, and is required together with `expires_after[seconds]`.

**expires\_after[seconds]** integer

**Possible values:** `>= 3600` and `<= 2592000`

The lifetime of the file in seconds, between 3600 (1 hour) and 2592000 (30 days). Required together with `expires_after[anchor]`. Omit both `expires_after` fields to keep the file permanently.

## Responses

- 200

OK, returns the uploaded `file object`.

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**id** stringrequired

The file identifier, of the form `file-api-...`, which can be referenced in chat completion requests.

**object** stringrequired

**Possible values:** [`file`]

The object type, which is always `file`.

**bytes** integerrequired

The size of the file in bytes.

**created\_at** integerrequired

The Unix timestamp (in seconds) of when the file was created.

**filename** stringrequired

The name of the file.

**purpose** stringrequired

**Possible values:** [`user_data`]

The intended purpose of the file.

**expires\_at** integer

The Unix timestamp (in seconds) of when the file expires. Only present when an expiration was set at upload time.

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
