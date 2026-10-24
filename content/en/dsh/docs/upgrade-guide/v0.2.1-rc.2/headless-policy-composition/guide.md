---
title: "Configure policy when replacing headless startup"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.2/headless-policy-composition/guide.md
fetched: 2026-10-24
---
# Configure policy when replacing headless startup

English | [中文](guide.zh.md)

## Change

The headless bundle reads `--add-dir` through `headlessStartup` before activating its sandbox policy. An overlay that disables `headless-startup` must also remove that dependency from `sandbox-policy`. Otherwise the policy and its dependent tools remain pending. Ordinary `dsh headless` invocations need no configuration change.

## Migration

1. In the overlay that disables `headless-startup`, supply the policy directly. Retain any existing policy settings in this replacement config:

   ```yaml
   - id: sandbox-policy
     inject: []
     config:
       mode: !!js process.env.DSH_PERMISSION_MODE ?? 'workspace-write'
       workspaceRoot: !!js process.cwd()
   ```

2. If the overlay keeps command-line startup but replaces `headless-runner` or `sandbox-policy`, retain their `headlessStartup` bindings from the [headless bundle](../../../../packages/bundle/headless/cordis.patch.yml).
3. Launch a small task through the custom profile and verify that its tools activate. If startup remains enabled, pass `--add-dir` and check that a write to the selected directory succeeds.
