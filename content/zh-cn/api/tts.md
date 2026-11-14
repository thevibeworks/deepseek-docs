---
title: "语音合成"
description: "把文本合成为语音，音频边合成边在响应体中流式返回。音色、语种、限制、错误与计费见 [语音合成指南](/zh-cn/guides/tts)。"
source: https://api-docs.deepseek.com/zh-cn/api/tts
fetched: 2026-11-14
---

# 语音合成

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/tts.md "在新标签页打开 Markdown")

```
POST /v1/tools/tts
```

把文本合成为语音，音频边合成边在响应体中流式返回。音色、语种、限制、错误与计费见 [语音合成指南](../guides/tts.md)。

如果要分段发送文本（例如模型还在生成时），请通过 WebSocket 连接同一路径（`wss://api.deepseek.com/v1/tools/tts`），协议见 [语音合成指南](../guides/tts.md)。

## Request

**[application/json]**

**Bodyrequired**

**text** stringrequired

要朗读的文本，不能为空。

**voice\_id** string

**Possible values:** `stella`, `tide`

**Default value:** `stella`

音色。`stella` 为女声，`tide` 为男声。

**format** string

**Possible values:** `wav`, `pcm`

**Default value:** `wav`

响应的音频格式。`wav` 返回 `audio/wav`；`pcm` 返回 24 kHz、16 位有符号、单声道的原始 PCM。

**filter\_markdown** boolean

**Default value:** `true`

朗读前是否去除文本中的 Markdown 格式。

## Responses

- 200

OK, 以流的形式返回音频。默认返回 WAV 文件；`format` 为 `pcm` 时，返回 24 kHz、16 位有符号、单声道的原始 PCM，`Content-Type` 为 `audio/pcm`。

**[audio/wav]**

- Schema
- Example

**[Schema]**

**Schema**

string

**[Example]**

```shell
（音频二进制数据）
```

Loading...
