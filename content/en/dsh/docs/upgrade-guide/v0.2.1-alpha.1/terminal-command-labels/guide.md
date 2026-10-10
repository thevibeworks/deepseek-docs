---
title: "Terminal command labels"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-alpha.1/terminal-command-labels/guide.md
fetched: 2026-10-10
---
# Terminal command labels

English | [中文](guide.zh.md)

## Change

`TerminalBlockLabels` from `@deepseek-ai/dsh-client-ui-primitives` requires a `commandLine(line: number): string` formatter. Previously, callers supplied no accessible name for command lines. Each horizontally overflowing line now uses this name for its keyboard-focusable group; lines that fit, including wrapped lines, add no Tab stop. This affects custom UI plugins that render `TerminalBlock`.

## Migration

1. Add `commandLine` to each labels object passed to `TerminalBlock`. The argument is the authored line number, starting at one.
2. Return a localized name, such as “Command line 1”, through the plugin's locale dictionary. Keep the original command text separate from this name.
3. Rebuild the plugin. Verify that a long command can receive keyboard focus and scroll with the arrow keys, and that a short or wrapped command adds no Tab stop.
