---
title: "SDK desktop tools and context"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.2/sdk-desktop-context/guide.md
fetched: 2026-10-26
---
# SDK desktop tools and context

English | [中文](guide.zh.md)

## Change

The existing `sdk` profile now includes `present`, `ask_user_question`, schedule tools, file-reference guidance and time context. It does not start a Web server. Native tool execution remains the default; select PTC through an [executor overlay](../tool-executor-plugins/guide.md). `sdk-minimal` is unchanged.

## Migration

1. Keep selecting `sdk`. Provide `onUserQuestion` (TypeScript) or `on_user_question` (Python) to answer built-in questions over the native protocol, or retain an in-process `user-questions/request` answerer; without one, the tool reports `NO_PROVIDER`.
2. Working directory and model still come from SDK initialization. The SDK profile does not mount the Web-specific checkout and GUI development context.
3. Custom compositions that need the previous model-visible tool/context roster can disable the `present`, `tool-ask-user`, `tool-schedule`, `file-reference-local`, `deliverable-file-references`, and `time-context` rows. Review any pinned prompts and tool schemas before upgrading.
