---
title: "文件解析"
description: "让模型基于你的文件回答问题，与 DeepSeek 网页端上传文件一致。分两步："
source: https://api-docs.deepseek.com/zh-cn/guides/document_parsing
fetched: 2026-11-14
---

# 文件解析

让模型基于你的文件回答问题，与 DeepSeek 网页端上传文件一致。分两步：

1. 把 PDF、Word、PowerPoint、图片等文件上传到 Files API，上传时指定解析方式。
2. 在对话请求中引用返回的 `file_id`。

文件在上传时完成解析，解析成功后才返回 `file_id`。

---

## 选择解析方式

两种方式的区别在于，模型能不能看到文档里的图：

| `purpose` | 模型得到的内容 | 适合的文档 |
| --- | --- | --- |
| `text_recognition` | 只有文字。文档里的图表、照片、示意图会被丢弃 | 以文字为主的文档，例如合同、论文、扫描的文字材料 |
| `rich_layout_recognition` | 文字，加上文档里的图：图表、照片、示意图会被裁出来，按原来的位置和文字一起交给模型 | 需要结合图来理解的文档，例如带图表的报告、幻灯片、带示意图的说明书 |

例如，一份财报里有一张营收趋势图，用户问“这张图说明了什么”：

- 用 `text_recognition` 解析，模型只读到正文文字，看不到这张图，只能根据正文作答。
- 用 `rich_layout_recognition` 解析，模型能看到这张图，可以结合正文回答。

文档里的图是在解析时自动识别并裁出的，不保证每张图都能被识别出来。没有被裁出的图，模型仍然看不到。

`rich_layout_recognition` 裁出的图会占用输入 Token，并计入每个请求的图片数量上限。不需要模型看图时，用 `text_recognition` 即可。

---

## 第一步：上传并解析文档

通过 `POST /files` 上传，也可以使用 [Anthropic 兼容接口](files_api.md#anthropic-compatible-files-api)。**`purpose` 字段必须放在 `file` 字段之前**。OpenAI Python SDK 会先发送表单字段、再发送文件，无需额外处理。

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

- 解析完成后才返回响应，解析期间不发送任何数据。请把客户端以及中间代理的超时时间设为上传时间加解析时间。
- 客户端中途断开时，解析仍会执行到结束；解析成功的文件照常保存并计费，之后可以在 `GET /files` 中看到。
- 上传失败的文件不会保存，也不计费。
- 上传的原始文件和解析结果都不支持下载。

---

## 第二步：在对话中引用文档

在 `deepseek-flash` 的对话请求中，在用户消息里引用上传返回的 `file_id`，模型即可基于文档回答问题。三个协议都支持：

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
          {"type": "text", "text": "总结这份文档的要点。"}
        ]
      }
    ]
  }'
```

Messages API 需要带上请求头 `anthropic-beta: files-api-2025-04-14`。

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
          {"type": "input_text", "text": "总结这份文档的要点。"}
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
          {"type": "text", "text": "总结这份文档的要点。"}
        ]
      }
    ]
  }'
```

- 用这两种 `purpose` 上传的文档不能当作图片使用：在图片块中引用会返回 `400`。
- 需要解析的文档只能通过 `file_id` 引用，不支持在请求中直接传入文件内容或文件的 URL。
- `rich_layout_recognition` 裁出的图片按原位置随文档一起交给模型，并计入每个请求的图片数量上限。
- 每个请求最多引用 20 个文档，文档文字合计不超过 8 MiB；同一个 `file_id` 引用多次时按多次计算。超过时返回 `400`。
- 多轮对话中，历史消息引用的 `file_id` 文档内容会完整保留在上下文中。上下文超长时返回 `400`，不会静默截断文档。
- 开启 [模型内容安全](safety.md) 后，文档中裁出的图片（`rich_layout_recognition`）会与请求中的其他图片一样经过审核。

---

## 纯文本、表格与电子书

以下文件不需要解析，上传时把 `purpose` 设为 `user_data`，引用方式与上文相同：

- 纯文本文件，例如 txt、md、csv、json 和代码文件。
- 表格（XLSX、XLS）与电子书（EPUB、MOBI），上传时会转换为 Markdown。不支持 AZW3 和带 DRM 的电子书。

原文件最大 32 MiB，文本内容最大 8 MiB。这类上传不计费。

在 Messages API 中，也可以不上传文件，直接在 `document` 块中传入文本：

```json
{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "文档内容"}}
```

---

## 限制与错误

| 限制 | 取值 |
| --- | --- |
| 文件格式 | PDF、Word（DOC、DOCX）、PowerPoint（PPT、PPTX），以及 PNG、JPEG、WebP、GIF、BMP、TIFF 等图片。格式由文件实际内容判断 |
| 文件大小 | 100 MiB，超过返回 `413` |
| 页数 | 1,000 页 |
| 上传 | 需在 120 秒内上传完成，否则返回 `408` |
| 解析时长 | 文件提交解析后 120 秒，超过返回 `504` |
| 每个账号同时进行的文档上传数 | 15，与 OCR API 分开计算 |

| 状态码 | 原因 |
| --- | --- |
| `400` | 文件无法解析或格式不支持、文件设有打开密码，或 `purpose` 写在 `file` 之后 |
| `408` | 上传过慢 |
| `413` | 文件过大 |
| `429` | 账号同时进行的文档上传数超过上限 |
| `500` | 解析结果不完整 |
| `503` | 服务繁忙，请稍后重试 |
| `504` | 解析超过时限 |

---

## 计费

- **上传解析时**：解析成功时，按文档页数一次性计费，价格见 [模型 & 价格](../quick_start/pricing.md#ocr-pricing)。
- **对话引用时**：不再收取解析费用；每次引用该文档的对话请求，按实际拼入上下文的输入 Token 计费。
