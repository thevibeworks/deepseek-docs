---
title: "Desktop font-size shortcuts reserve custom key combinations"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-alpha.2/desktop-font-size-shortcuts/guide.md
fetched: 2026-10-14
---
# Desktop font-size shortcuts reserve custom key combinations

English | [中文](guide.zh.md)

## Change

Desktop reserves `Cmd`/`Ctrl` + `=` (including `Shift` + `=` for `+`) and `Cmd`/`Ctrl` + `-` to adjust text, code, and terminal font sizes together. Use `Cmd` on macOS and `Ctrl` on Windows and Linux. Custom bindings using these combinations, including overlapping two-key chords, remain saved but no longer execute. Web shortcut behavior is unchanged.

## Migration

1. Open Settings → General → Keyboard shortcuts in Desktop and find any custom binding marked as conflicting with a font-size shortcut.
2. Record a nonconflicting combination for that action, or choose **Remove** to disable its keyboard shortcut. **Restore default** is available when the action's default does not conflict.
3. Try the reassigned action, then press `Cmd`/`Ctrl` + `=` and `Cmd`/`Ctrl` + `-`. Confirm that all three font sizes change in Settings and remain saved after reopening Desktop.
