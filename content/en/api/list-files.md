---
title: "List Files"
description: "Returns a list of files that belong to the user, with cursor-based pagination."
source: https://api-docs.deepseek.com/api/list-files
fetched: 2026-08-23
---

# List Files

```
GET /files
```

Returns a list of files that belong to the user, with cursor-based pagination.

## Request

**Query Parameters**

**after** string

A `file_id` cursor for pagination. Returns files listed after this one.

**limit** integer

**Possible values:** `>= 1` and `<= 1000`

**Default value:** `1000`

The number of files to return. Must be between 1 and 1000.

**order** string

**Possible values:** [`asc`, `desc`]

**Default value:** `asc`

Sort order by creation time. `asc` for ascending, `desc` for descending.

**purpose** string

**Possible values:** [`user_data`]

Only return files with the given purpose. Only `user_data` is supported.

## Responses

- 200

OK, returns a list of `file object`.

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**object** stringrequired

**Possible values:** [`list`]

The object type, which is always `list`.

**dataobject[]required**

The list of file objects.

- Array [

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

- ]

**first\_id** string

The ID of the first file in the list. Useful as a pagination cursor.

**last\_id** string

The ID of the last file in the list. Useful as a pagination cursor.

**has\_more** booleanrequired

Whether there are more files beyond this page.

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
