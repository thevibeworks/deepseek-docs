---
title: "Explicitly subscribe to account identity changes"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-alpha.2/deepseek-account-identity-watch/guide.md
fetched: 2026-10-14
---
# Explicitly subscribe to account identity changes

English | [中文](guide.zh.md)

## Change

The public `DeepSeekAccount.watch(signal)` method previously emitted a snapshot when a profile read first supplied or changed the cached Platform user ID. It now emits account-state changes only by default. Plugins that use this stream to refresh `getPlatformSession()` must opt into identity changes. Credential replacement and sign-in state changes still notify every subscriber.

## Migration

1. Find calls to `deepseekAccount.watch(signal)` in plugins that refresh the Platform session or synchronize its user ID.
2. Change those calls to `deepseekAccount.watch(signal, true)`. Leave account UI subscriptions that only need sign-in and credential state unchanged.
3. Confirm that a ready `getProfile()` result whose user ID first appears or changes wakes the subscription and causes it to re-read `getPlatformSession()`. Repeated reads with the same ID do not emit another identity notification.
