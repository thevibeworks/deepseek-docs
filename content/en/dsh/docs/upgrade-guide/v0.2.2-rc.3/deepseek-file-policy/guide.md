---
title: "Resolve the file policy for DeepSeekFileStore"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-rc.3/deepseek-file-policy/guide.md
fetched: 2026-11-21
---
# Resolve the file policy for DeepSeekFileStore

English | [中文](guide.zh.md)

## Change

The published `DeepSeekFilePolicy` type now requires `uploadConcurrency`, `uploadMaxRetries`, `uploadRetryDelayMs`, and `uploadTimeoutMs`. This affects TypeScript callers that construct their own policy for `DeepSeekFileStore`.

## Migration

1. Import `resolveAdapterOptions` from `@deepseek-ai/dsh-llm-deepseek`. Pass `resolveAdapterOptions(options).filePolicy` where you previously assembled a policy. To carry over custom expiry, refresh and cleanup values, supply `fileExpiresAfterSeconds`, `fileRefreshMarginSeconds` and `fileQuotaCleanupBatch` in `options`.
2. Type-check the caller and upload an image using `ensureUploaded`. The returned record contains its Files API id.
