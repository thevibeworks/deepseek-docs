---
title: "DeepSeek image upload timeout"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-rc.2/deepseek-files-timeout/guide.md
fetched: 2026-11-14
---
# DeepSeek image upload timeout

English | [中文](guide.zh.md)

## Change

The default `filesApiTimeoutMs` falls from 60,000 to 20,000 milliseconds. After an upload times out, the adapter sends inline images for the next request that needs an upload. Further timeouts double the number of requests skipped. A successful upload resets the count.

## Migration

If your gateway needs the previous deadline, set `filesApiTimeoutMs: 60000` on the DeepSeek provider in the active profile’s `cordis.patch.yml`. Existing explicit values take effect as configured. Run `dsh --profile <profile> --dump-config` and check the value on the provider entry.
