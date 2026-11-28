---
title: "Voice input recognizes in the cloud by default"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.3-alpha.2/voice-input-cloud-default/guide.md
fetched: 2026-11-28
---
# Voice input recognizes in the cloud by default

English | [中文](guide.zh.md)

## Change

The experimental voice input bundle set `speech-to-text.defaultProvider` to `sensevoice-local`, so recordings were recognized on the machine running DSH. It now sets `defaultProvider: auto` with `autoOrder: [deepseek-asr, sensevoice-local]` and adds the DeepSeek cloud provider: while a DeepSeek account is signed in or a DeepSeek API key is configured, recordings are sent to the DeepSeek speech recognition API and billed to that credential; otherwise the local SenseVoice provider is used. This affects users who enabled the bundle without choosing a recognizer in its details, have a DeepSeek credential, and expect recordings to stay on that machine. A recognizer chosen in the bundle details is kept.

## Migration

1. To keep local recognition, open Plugins, open the Voice input details, and choose SenseVoiceSmall (INT8) local recognition under the recognizer setting. This writes `defaultProvider: sensevoice-local` into the `speech-to-text` entry of the profile patch, `$DSH_HOME/profiles/<profile>/cordis.patch.yml`.
2. To confirm, hover the microphone in the composer: the tooltip reads Dictate without cloud recognition, and the details name the local recognizer as the one in use.
