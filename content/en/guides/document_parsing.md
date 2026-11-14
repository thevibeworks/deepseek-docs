---
title: "File Parsing"
description: "Have the model answer questions based on your files, like uploading files in DeepSeek Chat. There are two steps:"
source: https://api-docs.deepseek.com/guides/document_parsing
fetched: 2026-11-14
---

# File Parsing

Have the model answer questions based on your files, like uploading files in DeepSeek Chat. There are two steps:

1. Upload a file such as a PDF, a Word or PowerPoint document or an image to the Files API, choosing how it is parsed.
2. Reference the returned `file_id` in a chat request.

The file is parsed during the upload, and a `file_id` is returned only after parsing succeeds.

---

## Choose a Parsing Purpose

The two purposes differ in whether the model can see the figures in the document:

| `purpose` | What the model gets | Suitable documents |
| --- | --- | --- |
| `text_recognition` | Text only. Charts, photos and diagrams in the document are dropped | Documents that are mostly text, such as contracts, papers and scanned text |
| `rich_layout_recognition` | Text plus the figures in the document: charts, photos and diagrams are cropped out and given to the model at their original positions in the text | Documents that need their figures to be understood, such as reports with charts, slides and manuals with diagrams |

For example, a financial report contains a revenue trend chart, and the user asks "What does this chart show?":

- Parsed with `text_recognition`, the model reads only the body text. It cannot see the chart and can answer only from the text.
- Parsed with `rich_layout_recognition`, the model sees the chart and can answer using it together with the text.

Figures are detected and cropped automatically during parsing, and not every figure is guaranteed to be detected. The model still cannot see a figure that was not cropped out.

Figures cropped by `rich_layout_recognition` use input tokens and count towards the limit on images per request. If the model does not need to see figures, use `text_recognition`.

---

## Step 1: Upload and Parse a Document

Upload with `POST /files`, or with the [Anthropic-compatible endpoint](files_api.md#anthropic-compatible-files-api). **Send the `purpose` field before the `file` field**. The OpenAI Python SDK sends form fields before files, so it needs no change.

```bash
curl https://api.deepseek.com/files \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -F purpose="text_recognition" \
  -F file="@report.pdf"
```

```json
{
  "id": "file-api-xxxxxxxxxxxxxxxx",
  "object": "file",
  "bytes": 1048576,
  "created_at": 1762790000,
  "filename": "report.pdf",
  "purpose": "text_recognition"
}
```

- The response arrives only after parsing, and nothing is sent while the file is being parsed. Set the timeout of your client, and of any proxy in between, to cover the upload time plus the parsing time.
- If the client disconnects, parsing still runs to the end. If it succeeds, the file is stored and billed, and it appears in `GET /files`.
- A failed upload is not stored and not billed.
- Neither the uploaded original file nor the parsing result can be downloaded.

---

## Step 2: Reference a Document in Chat

Reference the returned `file_id` in a user message of a chat request with `deepseek-flash`, and the model answers questions based on the document. All three protocols support it:

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "document", "source": {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"}},
          {"type": "text", "text": "Summarize the key points of this document."}
        ]
      }
    ]
  }'
```

The Messages API requires the header `anthropic-beta: files-api-2025-04-14`.

**[Responses]**

```bash
curl https://api.deepseek.com/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "input_file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
          {"type": "input_text", "text": "Summarize the key points of this document."}
        ]
      }
    ]
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
          {"type": "text", "text": "Summarize the key points of this document."}
        ]
      }
    ]
  }'
```

- A document uploaded with either of these purposes cannot be used as an image: referencing it in an image block returns `400`.
- A document that needs parsing can be referenced only by `file_id`. Passing the file content or a file URL in the request is not supported.
- Images cropped by `rich_layout_recognition` are given to the model at their original positions, and count towards the limit on images per request.
- A request may reference at most 20 documents, and their text may total at most 8 MiB. Repeated references to the same `file_id` count separately. Beyond these limits the request returns `400`.
- Across turns in a conversation, the full parsed content of referenced `file_id` documents is kept in context. If the context is too long, the request returns `400`; documents are not truncated silently.
- With [model content safety](safety.md) enabled, the images cropped from documents (`rich_layout_recognition`) are reviewed like other images in the request.

---

## Plain Text, Spreadsheets and Ebooks

The following files need no parsing. Upload them with `purpose` set to `user_data` and reference them as described above:

- Plain-text files, such as txt, md, csv, json and source code files.
- Spreadsheets (XLSX, XLS) and ebooks (EPUB, MOBI), which are converted to Markdown during the upload. AZW3 and DRM-protected ebooks are not supported.

The original file may be at most 32 MiB, and its text at most 8 MiB. These uploads are not billed.

In the Messages API, you can also pass text directly in a `document` block without uploading a file:

```json
{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "The document text"}}
```

---

## Limits and Errors

| Limit | Value |
| --- | --- |
| File format | PDF, Word (DOC, DOCX), PowerPoint (PPT, PPTX), and images such as PNG, JPEG, WebP, GIF, BMP and TIFF. The format is detected from the actual file content |
| File size | 100 MiB. A larger file returns `413` |
| Pages | 1,000 pages |
| Upload | The upload must finish within 120 seconds; otherwise the request returns `408` |
| Parsing time | 120 seconds after the file has been submitted; beyond that the request returns `504` |
| Document uploads in progress per account | 15, counted separately from the OCR API |

| Status | Cause |
| --- | --- |
| `400` | The file cannot be parsed or its format is not supported, the file is password-protected, or `purpose` was sent after `file` |
| `408` | The upload was too slow |
| `413` | The file is too large |
| `429` | Your account has too many document uploads in progress |
| `500` | The parsing result is incomplete |
| `503` | The service is busy. Retry later |
| `504` | Parsing took longer than the time limit |

---

## Billing

- **At upload**: billed once per page of the document, only when parsing succeeds, at the price in [Models & Pricing](../quick_start/pricing.md#ocr-pricing).
- **In chat**: parsing is not billed again. Each chat request that references the document is billed for its input tokens at the model's input price.
