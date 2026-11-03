---
title: "Subagent reasoning overrides require an explicit route"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-alpha.2/subagent-explicit-reasoning/guide.md
fetched: 2026-11-03
---
# Subagent reasoning overrides require an explicit route

English | [中文](guide.zh.md)

## Change

Delegation tools with model selection enabled reject `reasoning_effort` unless the same call supplies both `provider` and `model`. Previously, an effort-only call could use a configured or inherited route. The rejection occurs before child creation.

An explicit provider/model pair without `reasoning_effort` uses the selected model's default effort, including when the pair matches the parent or configured child route. Previously, the unchanged route could retain a configured or parent effort. Omitting all three tool fields preserves the configured child defaults and existing fallback behavior.

## Migration

1. Update prompts, skills, and tool-call producers that send only `reasoning_effort`: include the authorized `provider` and `model`, or omit all three fields to use the default child selection. Query `list_subagent_models` for authorized routes and supported effort ids.
2. To preserve a specific effort while selecting a route, pass it explicitly as `reasoning_effort`.
3. Confirm an effort-only call returns a missing-route error without starting a child. For a complete route, check the child's logged `request/header` configuration: an omitted effort follows that model's default rather than the parent's selected effort.
