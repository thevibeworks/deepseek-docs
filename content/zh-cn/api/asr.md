---
title: "语音识别"
description: "把音频文件识别为文本。整段音频在一次请求中上传，返回完整的识别结果。语种、限制、错误与计费见 [语音识别指南](/zh-cn/guides/asr)。"
source: https://api-docs.deepseek.com/zh-cn/api/asr
fetched: 2026-11-14
---

# 语音识别

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/asr.md "在新标签页打开 Markdown")

```
POST /v1/tools/asr
```

把音频文件识别为文本。整段音频在一次请求中上传，返回完整的识别结果。语种、限制、错误与计费见 [语音识别指南](../guides/asr.md)。

## Request

**[multipart/form-data]**

**Bodyrequired**

**file** binaryrequired

音频文件：16 位 PCM WAV 或 Ogg Opus。限制见 [语音识别指南](../guides/asr.md)。

## Responses

- 200

OK, 返回识别结果。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**request\_id** stringrequired

请求 ID。

**text** stringrequired

识别出的文本。

**duration\_ms** integerrequired

音频时长，单位为毫秒。

**[Example]**

```json
{
  "request_id": "0b8c1c7e-3c0e-4d0f-9d3a-5f2a6f7e8b90",
  "text": "今天上海的天气怎么样？",
  "duration_ms": 3200
}
```

Loading...
