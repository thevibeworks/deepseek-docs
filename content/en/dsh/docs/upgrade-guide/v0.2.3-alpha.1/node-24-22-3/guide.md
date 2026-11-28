---
title: "Node.js 24.22.3 or 26.13.1 is required"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.3-alpha.1/node-24-22-3/guide.md
fetched: 2026-11-28
---
# Node.js 24.22.3 or 26.13.1 is required

English | [中文](guide.zh.md)

## Change

DSH requires Node.js 24.22.3 or a newer 24.x release, or Node.js 26.13.1 or newer (`engines.node` is `^24.22.3 || >=26.13.1`). These are the first releases whose bundled undici includes the November 2026 security fixes. The previous release supported Node.js 24.9 and newer, including every Node.js 26 release. This change affects npm installations, source checkouts, and the Python SDK's explicit `DSH_RUNTIME_MODE=node` development carrier. Packaged desktop applications and the Python SDK's bundled executable provide their own Node.js 24.22.3 runtime.

## Migration

1. Upgrade the Node.js installation used to start DSH to version 24.22.3 or a newer 24.x release, or to 26.13.1 or newer. Update Node version pins in development environments, containers, and CI jobs.
2. Run `node --version` in the same environment and confirm that it reports 24.22.3 or a newer 24.x release, or 26.13.1 or newer.
3. For a source checkout, run `pnpm install`. Start DSH with the profile you normally use and confirm that it starts successfully.
