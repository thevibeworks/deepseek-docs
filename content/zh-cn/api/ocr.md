---
title: "OCR"
description: "识别 PDF、Word、PowerPoint 文档或图片中的文字，按页返回识别结果。文件不会存入 Files API。限制、错误与计费见 [OCR 指南](/zh-cn/guides/ocr)。"
source: https://api-docs.deepseek.com/zh-cn/api/ocr
fetched: 2026-11-14
---

# OCR

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/ocr.md "在新标签页打开 Markdown")

```
POST /v1/tools/ocr
```

识别 PDF、Word、PowerPoint 文档或图片中的文字，按页返回识别结果。文件不会存入 Files API。限制、错误与计费见 [OCR 指南](../guides/ocr.md)。

## Request

**[multipart/form-data]**

**Bodyrequired**

**file** binaryrequired

要识别的文件，需带文件名。支持的格式与限制见 [OCR 指南](../guides/ocr.md)。

**purpose** stringrequired

**Possible values:** `text_recognition`, `rich_layout_recognition`

`text_recognition`：不含图片的 Word、PowerPoint 直接提取文字，其他文件逐页识别；`rich_layout_recognition`：所有文件都逐页识别。输出见 [OCR 指南](../guides/ocr.md#response)。

## Responses

- 200

OK, 返回每一页的识别结果。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

本次识别的 ID，形如 `ocr-...`。

**object** stringrequired

**Possible values:** `ocr.result`

对象类型，固定为 `ocr.result`。

**created** integerrequired

识别创建时的 Unix 时间戳（秒）。

**purpose** stringrequired

**Possible values:** `text_recognition`, `rich_layout_recognition`

请求中的 `purpose`。

**page\_count** integerrequired

页数，等于 `pages` 的长度。

**pages**

object[]

required

每一页的识别结果，按页序排列。

- Array [

**index** integerrequired

页码，从 0 开始。

**text** stringrequired

该页的模型原始输出，不做任何清理。

**finish\_reason** stringrequired

**Possible values:** `stop`, `length`

`stop` 表示该页完整识别；`length` 表示输出达到上限，该页文本不完整。

- ]

**usage**

object

required

所有页的 Token 用量，仅供参考，不用于计费。

**input\_tokens** integerrequired

所有页的 OCR 输入 Token，仅供参考，不用于计费。

**output\_tokens** integerrequired

所有页的 OCR 输出 Token，仅供参考，不用于计费。

**total\_tokens** integerrequired

`input_tokens` 与 `output_tokens` 之和。

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
      "text": "DeepSeek API\n\nDeepSeek API 使用与 OpenAI、Anthropic 兼容的 API 格式。",
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
