---
title: "Select interaction participation for non-page clients"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-alpha.2/operator-connect/guide.md
fetched: 2026-10-14
---
# Select interaction participation for non-page clients

English | [中文](guide.zh.md)

## Change

Non-page Connection installations default to `interactions: 'none'`. They do not open `$events`, and `$on()` and the generation-recovery helper `$stream()` are unavailable in that mode. Generated unary and raw stream methods remain usable. Browser authentication, existing browser Cookies, the shared Peer, and recovery behavior are unchanged; browsers need no reauthentication.

## Migration

1. Exchange the launch token at `GET /connect?token=<launch-token>&interactions=none` with manual redirect handling. Keep the returned API Cookie in client-owned storage and use it for HTTP and the lifecycle WebSocket at the returned 302 Location. HTTP need not wait for the socket to open.
2. For passive streaming, call the generated raw stream method directly rather than `$stream()`. After lifecycle-socket closure or Host restart, perform a new connect before retrying.
3. If the caller intentionally answers forwarded interactions, request `interactions=answer` and install Connection with that same mode. Confirm passive callers are refused at both event endpoints while the answering caller can subscribe.
