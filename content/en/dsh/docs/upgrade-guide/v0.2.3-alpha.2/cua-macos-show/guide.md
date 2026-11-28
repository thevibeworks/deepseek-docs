---
title: "Showing a macOS app or window"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.3-alpha.2/cua-macos-show/guide.md
fetched: 2026-11-28
---
# Showing a macOS app or window

English | [中文](guide.zh.md)

## Change

`app.show()` makes a running application visible. If it has no visible or recoverable minimized window, it asks the app to reopen once. The app may reuse a window or create another one. `window.show()` only targets the original window ID and fails if it is no longer usable. Both return `dispatched: false` when the window is already visible. A Stage Manager thumbnail is added to the active group before the helper confirms visibility.

## Migration

1. Call `app.show()` to display the app after its last window was closed. Select the returned `windowId` with `app.getWindow(id)`.
2. Keep using `window.show()` to restore a particular window. If it is closed, use `app.show()` when any window of that app will do. Use `app.activate()` when the app should keep keyboard focus.
