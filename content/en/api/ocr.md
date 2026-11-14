---
title: "OCR"
description: "Recognize the text in a PDF, Word or PowerPoint document or in an image, and return the result page by page. The file is not stored in the Files API. See the [OCR guide](/guides/ocr) for the limits, errors and billing."
source: https://api-docs.deepseek.com/api/ocr
fetched: 2026-11-14
---

# OCR

[Open Markdown](https://api-docs.deepseek.com/api/ocr.md "Open Markdown in a new tab")

```
POST /v1/tools/ocr
```

Recognize the text in a PDF, Word or PowerPoint document or in an image, and return the result page by page. The file is not stored in the Files API. See the [OCR guide](../guides/ocr.md) for the limits, errors and billing.

## Request

**[multipart/form-data]**

**Bodyrequired**

**file** binaryrequired

The file to recognize, sent with a file name. See the [OCR guide](../guides/ocr.md) for the supported formats and limits.

**purpose** stringrequired

**Possible values:** `text_recognition`, `rich_layout_recognition`

`text_recognition` extracts text directly from Word and PowerPoint files without images and recognizes other files page by page. `rich_layout_recognition` recognizes every file page by page. See the [OCR guide](../guides/ocr.md#response) for the output.

## Responses

- 200

OK, returns the recognition result of every page.

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

The recognition ID, of the form `ocr-...`.

**object** stringrequired

**Possible values:** `ocr.result`

The object type, which is always `ocr.result`.

**created** integerrequired

The Unix timestamp (in seconds) of when the recognition was created.

**purpose** stringrequired

**Possible values:** `text_recognition`, `rich_layout_recognition`

The `purpose` of the request.

**page\_count** integerrequired

The number of pages, equal to the length of `pages`.

**pages**

object[]

required

The recognition result of every page, in page order.

- Array [

**index** integerrequired

The page number, starting from 0.

**text** stringrequired

The raw model output for the page, without any cleanup.

**finish\_reason** stringrequired

**Possible values:** `stop`, `length`

`stop` when the page was recognized completely; `length` when the output reached the limit and the page text is incomplete.

- ]

**usage**

object

required

The token usage of all pages. For reference only; not used for billing.

**input\_tokens** integerrequired

The OCR input tokens of all pages. For reference only; not used for billing.

**output\_tokens** integerrequired

The OCR output tokens of all pages. For reference only; not used for billing.

**total\_tokens** integerrequired

The sum of `input_tokens` and `output_tokens`.

**[Example]**

```json
{
  "id": "ocr-9b2f4c1e-5d7a-4e3b-8f21-6c0a9d4e7b12",
  "object": "ocr.result",
  "created": 1762790000,
  "purpose": "text_recognition",
  "page_count": 1,
  "pages": [
    {
      "index": 0,
      "text": "DeepSeek API\n\nThe DeepSeek API uses an API format compatible with OpenAI and Anthropic.",
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "input_tokens": 1536,
    "output_tokens": 412,
    "total_tokens": 1948
  }
}
```

Loading...
