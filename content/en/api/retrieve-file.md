---
title: "Retrieve File"
description: "Returns information about a specific file."
source: https://api-docs.deepseek.com/api/retrieve-file
fetched: 2026-10-31
---

# Retrieve File

[Open Markdown](https://api-docs.deepseek.com/api/retrieve-file.md "Open Markdown in a new tab")

```
GET /files/:file_id
```

Returns information about a specific file.

## Request

**Path Parameters**

**file\_id** stringrequired

The ID of the file to retrieve.

## Responses

- 200

OK, returns the `file object`.

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

The file identifier, of the form `file-api-...`, which can be referenced in chat completion requests.

**object** stringrequired

**Possible values:** `file`

The object type, which is always `file`.

**bytes** integerrequired

The size of the file in bytes.

**created\_at** integerrequired

The Unix timestamp (in seconds) of when the file was created.

**filename** stringrequired

The name of the file.

**purpose** stringrequired

**Possible values:** `user_data`

The intended purpose of the file.

**expires\_at** integer

The Unix timestamp (in seconds) of when the file expires. Only present when an expiration was set at upload time.

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
