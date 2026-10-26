---
title: "Node.js 24 is required"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.2/node-24/guide.md
fetched: 2026-10-26
---
# Node.js 24 is required

English | [中文](guide.zh.md)

## Change

DSH requires Node.js 24.9 or newer. The previous release also supported Node.js 22.19 and newer releases in the 22.x line. This change affects npm installations, source checkouts, and the Python SDK's explicit `DSH_RUNTIME_MODE=node` development carrier. Packaged desktop applications and the Python SDK's bundled executable provide their own runtime.

## Migration

1. Upgrade the Node.js installation used to start DSH to version 24.9 or newer. Update Node version pins in development environments, containers, and CI jobs.
2. Run `node --version` in the same environment and confirm that it reports version 24.9 or newer.
3. For a source checkout, run `pnpm install`. Start DSH with the profile you normally use and confirm that it starts successfully.
