---
title: "Chat `ProcessActivity` adds `context`"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-alpha.3/chat-process-activity-context/guide.md
fetched: 2026-11-07
---
# Chat `ProcessActivity` adds `context`

English | [中文](guide.zh.md)

## Change

`ProcessActivity`, exported from `@deepseek-ai/dsh-client-ui-chat/client`, gains the member `context`. A closed process group whose members are all Context injections reports it as its only category. `ProcessActivitySummary.running` is now typed as the new exported `RunningProcessActivity`, which excludes `context`. This affects extensions that switch exhaustively over `ProcessActivity` or map every member to a label or icon.

## Migration

1. Add a `context` branch wherever code handles every `ProcessActivity` member, for example in a `Record<ProcessActivity, …>` or a `switch` ending in `assertNever`.
2. Type values read from `summary.running` as `RunningProcessActivity` when they need not cover `context`.
3. Run the extension's typecheck and confirm it compiles without a missing-member error.
