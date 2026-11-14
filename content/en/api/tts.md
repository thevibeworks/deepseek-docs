---
title: "Text to Speech"
description: "Convert text into speech. The audio is streamed in the response body as it is synthesized. See the [Text to Speech guide](/guides/tts) for the voices, languages, limits, errors and billing."
source: https://api-docs.deepseek.com/api/tts
fetched: 2026-11-14
---

# Text to Speech

[Open Markdown](https://api-docs.deepseek.com/api/tts.md "Open Markdown in a new tab")

```
POST /v1/tools/tts
```

Convert text into speech. The audio is streamed in the response body as it is synthesized. See the [Text to Speech guide](../guides/tts.md) for the voices, languages, limits, errors and billing.

To send the text in chunks, for example while a model is still generating it, connect to the same path over WebSocket (`wss://api.deepseek.com/v1/tools/tts`). The WebSocket protocol is described in the [Text to Speech guide](../guides/tts.md).

## Request

**[application/json]**

**Bodyrequired**

**text** stringrequired

The text to read. Must not be empty.

**voice\_id** string

**Possible values:** `stella`, `tide`

**Default value:** `stella`

The voice. `stella` is a female voice and `tide` is a male voice.

**format** string

**Possible values:** `wav`, `pcm`

**Default value:** `wav`

The audio format of the response. `wav` returns `audio/wav`; `pcm` returns raw 16-bit signed mono PCM at 24 kHz.

**filter\_markdown** boolean

**Default value:** `true`

Whether to remove Markdown formatting from the text before reading it.

## Responses

- 200

OK, returns the audio as a stream. By default the body is a WAV file. When `format` is `pcm`, the body is raw 16-bit signed mono PCM at 24 kHz and the `Content-Type` is `audio/pcm`.

**[audio/wav]**

- Schema
- Example

**[Schema]**

**Schema**

string

**[Example]**

```shell
(binary audio)
```

Loading...
