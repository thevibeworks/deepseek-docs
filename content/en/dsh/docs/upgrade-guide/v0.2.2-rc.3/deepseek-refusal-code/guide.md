---
title: "DeepSeek content refusal error code"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-rc.3/deepseek-refusal-code/guide.md
fetched: 2026-11-28
---
# DeepSeek content refusal error code

English | [中文](guide.zh.md)

## Change

When DeepSeek ends a model stream with `stop_reason: "refusal"`, DSH reports `CONTENT_REFUSED` in the LLM error finish and in the failed turn's `turn/end` error. Previously, the adapter reported `MALFORMED_RESPONSE` for this stop reason.

## Migration

1. Handle `CONTENT_REFUSED` in code that classifies LLM error finishes or `turn/end` errors. Tell the user that the provider refused the request.
2. Replay a Messages stream ending in `refusal` and check that your handler takes the refusal path.
