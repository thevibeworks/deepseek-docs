---
title: "OCR"
description: "OCR API 识别 PDF、Word、PowerPoint 文档或图片中的文字，按页返回识别结果。文件不会存入 Files API，也不会交给对话模型。如果要让模型基于文档回答问题，请参阅 文件解析。"
source: https://api-docs.deepseek.com/zh-cn/guides/ocr
fetched: 2026-11-14
---

# OCR

OCR API 识别 PDF、Word、PowerPoint 文档或图片中的文字，按页返回识别结果。文件不会存入 Files API，也不会交给对话模型。如果要让模型基于文档回答问题，请参阅 [文件解析](document_parsing.md)。

`POST https://api.deepseek.com/v1/tools/ocr`

完整的请求与响应结构见 [OCR API 参考](../api/ocr.md)。

---

## 请求

使用 `multipart/form-data` 发送两个字段，均为必填；传入其他字段会返回 `400` 错误。

| 字段 | 说明 |
| --- | --- |
| `file` | 要识别的文件，需带文件名。支持 PDF、Word（DOC、DOCX）、PowerPoint（PPT、PPTX），以及 PNG、JPEG、WebP、GIF、BMP、TIFF 等图片。格式由文件实际内容判断 |
| `purpose` | `text_recognition`：不含图片的 Word、PowerPoint 直接提取文字，其他文件逐页识别；`rich_layout_recognition`：所有文件都逐页识别。两者的输出见 [响应](#response) |

```bash
curl https://api.deepseek.com/v1/tools/ocr \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -F purpose="text_recognition" \
  -F file="@document.pdf"
```

### 限制

| 限制 | 取值 |
| --- | --- |
| 文件大小 | 100 MiB，超过返回 `413` |
| 页数 | 1,000 页 |
| 上传 | 需在 120 秒内上传完成，且中途停顿不超过 30 秒，否则返回 `408` |
| 总时长 | 从开始上传算起 180 秒，包括上传、识别与返回结果 |

---

## 响应

识别过程中，服务端持续发送换行符保持连接，识别完成后以一个 JSON 对象返回结果。换行符属于 JSON 的前导空白，整个响应体可以直接按 JSON 解析。

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

| 字段 | 说明 |
| --- | --- |
| `id` | 本次识别的 ID |
| `purpose` | 请求中的 `purpose` |
| `page_count` | 页数，等于 `pages` 的长度 |
| `pages[].index` | 页码，从 0 开始 |
| `pages[].text` | 该页的模型原始输出，不做任何清理 |
| `pages[].finish_reason` | `stop`；输出达到上限时为 `length`，该页文本不完整 |
| `usage` | 所有页的输入与输出 Token，仅供参考，不用于计费 |

逐页识别得到的文本中保留 `<｜ref｜>`、`<｜box｜>` 等特殊标记及坐标，例如 `<｜ref｜>标题<｜/ref｜><｜box｜>[[52, 40, 948, 96]]<｜/box｜>`，你可以据此定位文字、自行裁切图片。直接提取文字的文档不带这些标记。

坐标为 `[[x1, y1, x2, y2]]`，即区域左上角与右下角的位置。原点在页面左上角，取值按页面宽高归一化到 0–1000：实际像素位置为 `x × 页面宽度 ÷ 1000` 与 `y × 页面高度 ÷ 1000`。

使用 `text_recognition` 时，不含图片的 Word、PowerPoint 文档会直接提取文字，结果中的用途仍为 `text_recognition`。

---

## 错误

上传阶段的错误以 HTTP 状态码返回：

| 状态码 | 原因 |
| --- | --- |
| `400` | 表单或 `purpose` 不合法，或文件无法处理 |
| `402` | 余额不足 |
| `408` | 上传过慢（见 [限制](#limits)） |
| `413` | 文件过大 |
| `429` | 账号同时进行的识别数超过上限（见 [限速](#rate-limits)） |
| `500` | 文件上传或提交识别失败 |
| `503` | 服务繁忙，请稍后重试 |
| `504` | 上传与提交超过总时长 |

识别开始后，状态码已经是 `200`。如果识别失败或超时，响应体不是识别结果，而是一个错误对象，请检查其中是否有 `error`：

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

请求在识别开始前失败时，也可能以 HTTP 错误状态返回同样的 `error.message`。

以下情况重试无法解决：

| 情况 | 处理方式 | `error.message` |
| --- | --- | --- |
| 文件设有打开密码 | 移除密码后重新上传 | `The file is password-protected and cannot be processed. Remove the password and upload it again.` |
| 文件无法解析、格式不支持，或图片无法解码 | 修复文件或转换为支持的格式后重新上传 | `Failed to recognize the file: the file could not be parsed or its format is not supported` `Failed to recognize the file: the file format is not supported` `Failed to recognize the file: the image could not be decoded` |
| 文档超过 1,000 页 | 上传不超过 1,000 页的文档 | `Failed to recognize the file: the document has more than 1000 pages` |
| 文件过大 | 上传不超过 100 MiB 的文件 | `file is too large: max 100 MiB` |
| 识别超时 | 发送更小的文件 | `OCR did not finish in time` `OCR did not finish within 180 seconds` |

以下情况是暂时性的，稍后重试即可：

| 情况 | 处理方式 | `error.message` |
| --- | --- | --- |
| 服务繁忙 | 稍后重试 | `The OCR service is temporarily unavailable. Please try again later.` |
| 服务内部错误 | 稍后重试 | `Internal Server Error` |

---

## 计费

| 计费单位 | 价格 |
| --- | --- |
| 每 1,000 页 | 1.5 元 |

按识别成功的页数（`page_count`）计费，识别失败或超时不计费。

客户端断开不会取消识别：文件接收完成后，识别会继续执行到结束，完成的照常计费。

---

## 限速

每个账号最多同时进行 15 个识别，与对话模型分开计算，超过返回 `429`。客户端断开后，未完成的识别仍然占用名额。
