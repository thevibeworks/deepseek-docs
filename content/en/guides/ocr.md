---
title: "OCR"
description: "The OCR API recognizes the text in a PDF, Word or PowerPoint document or in an image, and returns the result page by page. The file is not stored in the Files API and is not passed to a chat model. To have the model answer questions about a document instead, see File Parsing."
source: https://api-docs.deepseek.com/guides/ocr
fetched: 2026-11-14
---

# OCR

The OCR API recognizes the text in a PDF, Word or PowerPoint document or in an image, and returns the result page by page. The file is not stored in the Files API and is not passed to a chat model. To have the model answer questions about a document instead, see [File Parsing](document_parsing.md).

`POST https://api.deepseek.com/v1/tools/ocr`

See the [OCR API Reference](../api/ocr.md) for the complete request and response schemas.

---

## Request

Send a `multipart/form-data` request with two fields. Both are required, and any other field returns a `400` error.

| Field | Description |
| --- | --- |
| `file` | The file to recognize, sent with a file name. Supported: PDF, Word (DOC, DOCX), PowerPoint (PPT, PPTX), and images such as PNG, JPEG, WebP, GIF, BMP and TIFF. The format is detected from the actual file content |
| `purpose` | `text_recognition`: Word and PowerPoint files without images have their text extracted directly, and other files are recognized page by page. `rich_layout_recognition`: every file is recognized page by page. See [Response](#response) for the output |

```bash
curl https://api.deepseek.com/v1/tools/ocr \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -F purpose="text_recognition" \
  -F file="@document.pdf"
```

### Limits

| Limit | Value |
| --- | --- |
| File size | 100 MiB. A larger file returns `413` |
| Pages | 1,000 pages |
| Upload | The upload must finish within 120 seconds, with no pause longer than 30 seconds; otherwise the request returns `408` |
| Total time | 180 seconds from the start of the upload, covering the upload, recognition and the result |

---

## Response

While the file is being recognized, the service sends newline characters to keep the connection alive, then sends the result as one JSON object. The newlines are leading whitespace, so the whole response body can be parsed as JSON.

```json
{
  "id": "ocr-9b2f4c1e-...",
  "object": "ocr.result",
  "created": 1762790000,
  "purpose": "text_recognition",
  "page_count": 2,
  "pages": [
    {"index": 0, "text": "...", "finish_reason": "stop"},
    {"index": 1, "text": "...", "finish_reason": "length"}
  ],
  "usage": {"input_tokens": 1536, "output_tokens": 412, "total_tokens": 1948}
}
```

| Field | Description |
| --- | --- |
| `id` | The recognition ID |
| `purpose` | The `purpose` of the request |
| `page_count` | The number of pages, equal to the length of `pages` |
| `pages[].index` | The page number, starting from 0 |
| `pages[].text` | The raw model output for the page, without any cleanup |
| `pages[].finish_reason` | `stop`, or `length` when the output reached the limit and the page text is incomplete |
| `usage` | The input and output tokens of all pages, for reference only; not used for billing |

Text recognized page by page keeps special tokens such as `<｜ref｜>` and `<｜box｜>` together with coordinates, for example `<｜ref｜>Title<｜/ref｜><｜box｜>[[52, 40, 948, 96]]<｜/box｜>`, so you can locate text and crop figures yourself. Documents whose text is extracted directly have no such tokens.

The coordinates are `[[x1, y1, x2, y2]]`: the top-left and bottom-right corners of the region. The origin is the top-left corner of the page, and values are normalized to 0–1000 by the page width and height: the pixel position is `x × page width ÷ 1000` and `y × page height ÷ 1000`.

With `text_recognition`, a Word or PowerPoint document without images has its text extracted directly instead of being recognized; the result still reports `text_recognition`.

---

## Errors

Errors during the upload return an HTTP status:

| Status | Cause |
| --- | --- |
| `400` | Invalid form or `purpose`, or the file cannot be processed |
| `402` | Insufficient balance |
| `408` | The upload was too slow (see [Limits](#limits)) |
| `413` | The file is too large |
| `429` | Your account has too many recognitions in progress (see [Rate Limits](#rate-limits)) |
| `500` | The file could not be uploaded or submitted for recognition |
| `503` | The service is busy. Retry later |
| `504` | The upload and submission took longer than the total time |

Once recognition has started, the status is already `200`. If recognition fails or times out, the response body is an error object instead of a result, so check whether it contains `error`:

```json
{
  "error": {
    "message": "OCR did not finish in time",
    "type": "gateway_timeout_error",
    "param": null,
    "code": "gateway_timeout_error"
  }
}
```

The same error messages can also be returned with an HTTP error status if the request fails before recognition starts.

These failures are not resolved by retrying:

| Case | What to do | `error.message` |
| --- | --- | --- |
| The file has an open password | Remove the password and upload it again | `The file is password-protected and cannot be processed. Remove the password and upload it again.` |
| The file cannot be parsed, its format is not supported, or an image cannot be decoded | Fix the file or convert it to a supported format, then upload it again | `Failed to recognize the file: the file could not be parsed or its format is not supported` `Failed to recognize the file: the file format is not supported` `Failed to recognize the file: the image could not be decoded` |
| The document has more than 1,000 pages | Send a document of at most 1,000 pages | `Failed to recognize the file: the document has more than 1000 pages` |
| The file is too large | Upload a file of at most 100 MiB | `file is too large: max 100 MiB` |
| Recognition timed out | Send a smaller file | `OCR did not finish in time` `OCR did not finish within 180 seconds` |

These failures are transient; retry the request later:

| Case | What to do | `error.message` |
| --- | --- | --- |
| The service is busy | Retry later | `The OCR service is temporarily unavailable. Please try again later.` |
| An internal error occurred | Retry later | `Internal Server Error` |

---

## Billing

| Billing unit | Price |
| --- | --- |
| Per 1,000 pages | $0.225 |

Billed by the number of pages recognized successfully (`page_count`). A recognition that fails or times out is not billed.

Disconnecting does not cancel a recognition: once the file has been received, the recognition runs to the end and is billed if it completes.

---

## Rate Limits

An account can have at most 15 recognitions in progress, counted separately from the chat models; beyond that a request returns `429`. After the client disconnects, an unfinished recognition still counts.
