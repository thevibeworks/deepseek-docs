---
title: "npm: @deepseek-ai/dsh"
source: https://www.npmjs.com/package/@deepseek-ai/dsh
fetched: 2026-11-28
---
# npm: @deepseek-ai/dsh

dsh CLI: profile launch, plugin management, and configuration inspection

```bash
npm install -g @deepseek-ai/dsh
```

- **latest**: `0.2.2-rc.5`
- **alpha**: `0.2.3-alpha.3`
- **next**: `0.2.2-rc.5`
- **license**: MIT
- **bin**: `dsh`
- **homepage**: https://github.com/deepseek-ai/deepseek-harness#readme

## Upgrade guides by release

Upgrade guides on `master` that are missing from a dist-tag's git tag
(`dsh-v<version>`). A guide's directory names the release you upgrade FROM,
not the release that carries it; a guide listed here was not in that
release's tree. Read the source at the tag before saying the release ships
or lacks the change itself.

- **alpha** (`0.2.3-alpha.3`): carries every guide on `master`.
- **latest** (`0.2.2-rc.5`): 86 of 231 guides on `master` are not in it:
  - `v0.2.2-rc.1/package-export-cleanup`
  - `v0.2.2-rc.1/ptc-bootstrap-protocol`
  - `v0.2.2-rc.1/ptc-inspect-output`
  - `v0.2.2-rc.1/ptc-scoped-repl-default`
  - `v0.2.2-rc.1/web-fetch-transport-error-codes`
  - `v0.2.2-rc.2/client-module-metadata`
  - `v0.2.2-rc.2/connection-page-peer`
  - `v0.2.2-rc.2/cordis-root-and-intercept-metadata`
  - `v0.2.2-rc.2/cua-agents-without-preset`
  - `v0.2.2-rc.2/cua-macos-provider`
  - `v0.2.2-rc.2/cua-partial-observations`
  - `v0.2.2-rc.2/deepseek-files-timeout`
  - `v0.2.2-rc.2/experimental-tool-error-codes`
  - `v0.2.2-rc.2/package-export-cleanup`
  - `v0.2.2-rc.2/python-ptc-removal`
  - `v0.2.2-rc.2/session-status-package`
  - `v0.2.2-rc.2/shared-search-filter`
  - `v0.2.2-rc.2/shell-fs-tool-error-codes`
  - `v0.2.2-rc.3/action-card-blocks`
  - `v0.2.2-rc.3/client-hmr-plugin-events-stream`
  - `v0.2.2-rc.3/cordis-inspect-tool`
  - `v0.2.2-rc.3/cordis-loader-entry-validation`
  - `v0.2.2-rc.3/create-worktree-tool-merged`
  - `v0.2.2-rc.3/deepseek-file-policy`
  - `v0.2.2-rc.3/deepseek-request-auth`
  - `v0.2.2-rc.3/forge-command-rules`
  - `v0.2.2-rc.3/forge-provider-hosts`
  - `v0.2.2-rc.3/profile-context-overlay-paths`
  - `v0.2.2-rc.3/ptc-mcp-image-values`
  - `v0.2.2-rc.3/ptc-output-limit`
  - `v0.2.2-rc.3/ptc-tool-result-inspection`
  - `v0.2.2-rc.3/session-fork-source`
  - `v0.2.2-rc.3/session-panel-entries`
  - `v0.2.2-rc.3/session-retain-conversation-facet`
  - `v0.2.2-rc.3/settings-section-plugins-page`
  - `v0.2.2-rc.3/subagent-initial-task-source`
  - `v0.2.2-rc.3/subagent-model-selection-live-setting`
  - `v0.2.2-rc.3/upstream-skills-base-row`
  - `v0.2.2-rc.3/working-directory-tool-removed`
  - `v0.2.2-rc.4/forge-rate-limited-failure`
  - `v0.2.2-rc.4/workspace-write-boundary-follows-root`
  - `v0.2.2-rc.5/archive-worktrees-without-sandbox-policy`
  - `v0.2.2-rc.5/compaction-summary-preview`
  - `v0.2.2-rc.5/cua-activity-helper`
  - `v0.2.2-rc.5/cua-held-inputs`
  - `v0.2.2-rc.5/cua-system-input`
  - `v0.2.2-rc.5/independent-action-cards`
  - `v0.2.2-rc.5/list-agents-capacity`
  - `v0.2.2-rc.5/office-single-skill`
  - `v0.2.2-rc.5/personalized-recommendations-bundle-retired`
  - `v0.2.2-rc.5/pi-image-resize-defaults`
  - `v0.2.2-rc.5/ptc-default-scoped-repl`
  - `v0.2.2-rc.5/sdk-prompt-time-zone`
  - `v0.2.2-rc.5/session-query-inspect-session-removed`
  - `v0.2.2-rc.5/system-prompt-integrations`
  - `v0.2.3-alpha.1/node-24-22-3`
  - `v0.2.3-alpha.2/apply-patch-default-on`
  - `v0.2.3-alpha.2/bundle-row-package-selection`
  - `v0.2.3-alpha.2/client-packages-dynamic-plugins`
  - `v0.2.3-alpha.2/conversation-focus-kinds`
  - `v0.2.3-alpha.2/cordis-inspect-providers-host-runner`
  - `v0.2.3-alpha.2/cua-macos-show`
  - `v0.2.3-alpha.2/cua-windows-partial-observations`
  - `v0.2.3-alpha.2/desktop-channel-convergence`
  - `v0.2.3-alpha.2/factory-content-roots`
  - `v0.2.3-alpha.2/forge-local-changes-head`
  - `v0.2.3-alpha.2/forge-review-lists-host-scope`
  - `v0.2.3-alpha.2/forge-viewer-list-rows`
  - `v0.2.3-alpha.2/general-settings-group-slots`
  - `v0.2.3-alpha.2/headless-session-preset`
  - `v0.2.3-alpha.2/hoc-slot-children-outlet`
  - `v0.2.3-alpha.2/invalid-tool-arguments-code`
  - `v0.2.3-alpha.2/list-item-roots`
  - `v0.2.3-alpha.2/office-tools-renamed-document`
  - `v0.2.3-alpha.2/react-19-client-runtime`
  - `v0.2.3-alpha.2/responsive-standard-props`
  - `v0.2.3-alpha.2/sdk-cordis-inspect`
  - `v0.2.3-alpha.2/session-panel-indicators`
  - `v0.2.3-alpha.2/slot-class-name-props`
  - `v0.2.3-alpha.2/sqlite-event-rows`
  - `v0.2.3-alpha.2/theme-standard-prop`
  - `v0.2.3-alpha.2/time-context-reminder`
  - `v0.2.3-alpha.2/tool-registry-roots`
  - `v0.2.3-alpha.2/voice-input-cloud-default`
  - `v0.2.3-alpha.2/windows-cua-identities`
  - `v0.2.3-alpha.2/workspace-changes-timeout`
- **next** (`0.2.2-rc.5`): 86 of 231 guides on `master` are not in it:
  - `v0.2.2-rc.1/package-export-cleanup`
  - `v0.2.2-rc.1/ptc-bootstrap-protocol`
  - `v0.2.2-rc.1/ptc-inspect-output`
  - `v0.2.2-rc.1/ptc-scoped-repl-default`
  - `v0.2.2-rc.1/web-fetch-transport-error-codes`
  - `v0.2.2-rc.2/client-module-metadata`
  - `v0.2.2-rc.2/connection-page-peer`
  - `v0.2.2-rc.2/cordis-root-and-intercept-metadata`
  - `v0.2.2-rc.2/cua-agents-without-preset`
  - `v0.2.2-rc.2/cua-macos-provider`
  - `v0.2.2-rc.2/cua-partial-observations`
  - `v0.2.2-rc.2/deepseek-files-timeout`
  - `v0.2.2-rc.2/experimental-tool-error-codes`
  - `v0.2.2-rc.2/package-export-cleanup`
  - `v0.2.2-rc.2/python-ptc-removal`
  - `v0.2.2-rc.2/session-status-package`
  - `v0.2.2-rc.2/shared-search-filter`
  - `v0.2.2-rc.2/shell-fs-tool-error-codes`
  - `v0.2.2-rc.3/action-card-blocks`
  - `v0.2.2-rc.3/client-hmr-plugin-events-stream`
  - `v0.2.2-rc.3/cordis-inspect-tool`
  - `v0.2.2-rc.3/cordis-loader-entry-validation`
  - `v0.2.2-rc.3/create-worktree-tool-merged`
  - `v0.2.2-rc.3/deepseek-file-policy`
  - `v0.2.2-rc.3/deepseek-request-auth`
  - `v0.2.2-rc.3/forge-command-rules`
  - `v0.2.2-rc.3/forge-provider-hosts`
  - `v0.2.2-rc.3/profile-context-overlay-paths`
  - `v0.2.2-rc.3/ptc-mcp-image-values`
  - `v0.2.2-rc.3/ptc-output-limit`
  - `v0.2.2-rc.3/ptc-tool-result-inspection`
  - `v0.2.2-rc.3/session-fork-source`
  - `v0.2.2-rc.3/session-panel-entries`
  - `v0.2.2-rc.3/session-retain-conversation-facet`
  - `v0.2.2-rc.3/settings-section-plugins-page`
  - `v0.2.2-rc.3/subagent-initial-task-source`
  - `v0.2.2-rc.3/subagent-model-selection-live-setting`
  - `v0.2.2-rc.3/upstream-skills-base-row`
  - `v0.2.2-rc.3/working-directory-tool-removed`
  - `v0.2.2-rc.4/forge-rate-limited-failure`
  - `v0.2.2-rc.4/workspace-write-boundary-follows-root`
  - `v0.2.2-rc.5/archive-worktrees-without-sandbox-policy`
  - `v0.2.2-rc.5/compaction-summary-preview`
  - `v0.2.2-rc.5/cua-activity-helper`
  - `v0.2.2-rc.5/cua-held-inputs`
  - `v0.2.2-rc.5/cua-system-input`
  - `v0.2.2-rc.5/independent-action-cards`
  - `v0.2.2-rc.5/list-agents-capacity`
  - `v0.2.2-rc.5/office-single-skill`
  - `v0.2.2-rc.5/personalized-recommendations-bundle-retired`
  - `v0.2.2-rc.5/pi-image-resize-defaults`
  - `v0.2.2-rc.5/ptc-default-scoped-repl`
  - `v0.2.2-rc.5/sdk-prompt-time-zone`
  - `v0.2.2-rc.5/session-query-inspect-session-removed`
  - `v0.2.2-rc.5/system-prompt-integrations`
  - `v0.2.3-alpha.1/node-24-22-3`
  - `v0.2.3-alpha.2/apply-patch-default-on`
  - `v0.2.3-alpha.2/bundle-row-package-selection`
  - `v0.2.3-alpha.2/client-packages-dynamic-plugins`
  - `v0.2.3-alpha.2/conversation-focus-kinds`
  - `v0.2.3-alpha.2/cordis-inspect-providers-host-runner`
  - `v0.2.3-alpha.2/cua-macos-show`
  - `v0.2.3-alpha.2/cua-windows-partial-observations`
  - `v0.2.3-alpha.2/desktop-channel-convergence`
  - `v0.2.3-alpha.2/factory-content-roots`
  - `v0.2.3-alpha.2/forge-local-changes-head`
  - `v0.2.3-alpha.2/forge-review-lists-host-scope`
  - `v0.2.3-alpha.2/forge-viewer-list-rows`
  - `v0.2.3-alpha.2/general-settings-group-slots`
  - `v0.2.3-alpha.2/headless-session-preset`
  - `v0.2.3-alpha.2/hoc-slot-children-outlet`
  - `v0.2.3-alpha.2/invalid-tool-arguments-code`
  - `v0.2.3-alpha.2/list-item-roots`
  - `v0.2.3-alpha.2/office-tools-renamed-document`
  - `v0.2.3-alpha.2/react-19-client-runtime`
  - `v0.2.3-alpha.2/responsive-standard-props`
  - `v0.2.3-alpha.2/sdk-cordis-inspect`
  - `v0.2.3-alpha.2/session-panel-indicators`
  - `v0.2.3-alpha.2/slot-class-name-props`
  - `v0.2.3-alpha.2/sqlite-event-rows`
  - `v0.2.3-alpha.2/theme-standard-prop`
  - `v0.2.3-alpha.2/time-context-reminder`
  - `v0.2.3-alpha.2/tool-registry-roots`
  - `v0.2.3-alpha.2/voice-input-cloud-default`
  - `v0.2.3-alpha.2/windows-cua-identities`
  - `v0.2.3-alpha.2/workspace-changes-timeout`

## Versions

- `0.2.3-alpha.3` -- 2026-11-28
- `0.2.3-alpha.2` -- 2026-11-22
- `0.2.3-alpha.1` -- 2026-11-22
- `0.2.2-rc.5` -- 2026-11-18
- `0.2.2-rc.4` -- 2026-11-17
- `0.2.2-rc.3` -- 2026-11-13
- `0.2.2-rc.2` -- 2026-11-12
- `0.2.2-rc.1` -- 2026-11-04
- `0.2.2-alpha.3` -- 2026-11-03
- `0.2.1-rc.5` -- 2026-10-29
- `0.2.2-alpha.2` -- 2026-10-27
- `0.2.1-rc.4` -- 2026-10-26
- `0.2.1-rc.3` -- 2026-10-23
- `0.2.1-rc.2` -- 2026-10-17
- `0.2.1-rc.1` -- 2026-10-17
- `0.2.1-alpha.5` -- 2026-10-16
- `0.2.1-alpha.4` -- 2026-10-15
- `0.2.1-alpha.3` -- 2026-10-14
- `0.2.1-alpha.2` -- 2026-10-09
- `0.2.1-alpha.1` -- 2026-10-03
- `0.2.0-rc.2` -- 2026-09-29
- `0.2.0-rc.1` -- 2026-09-28
- `0.1.7-rc.2` -- 2026-09-24
- `0.1.7-rc.1` -- 2026-09-23
- `0.1.7-alpha.2` -- 2026-09-22
- `0.1.7-alpha.1` -- 2026-09-22
- `0.1.5-rc.3` -- 2026-09-22
- `0.1.6-alpha.2` -- 2026-09-17
- `0.1.6-alpha.1` -- 2026-09-15
- `0.1.5-rc.2` -- 2026-09-10
- `0.1.5-rc.1` -- 2026-09-10
- `0.1.5-alpha.2` -- 2026-09-09
- `0.1.5-alpha.1` -- 2026-09-08
- `0.1.3-alpha.2` -- 2026-09-07
- `0.1.2-rc.1` -- 2026-09-03
- `0.1.2-alpha.5` -- 2026-09-02
- `0.1.2-alpha.4` -- 2026-09-01
- `0.1.2-alpha.3` -- 2026-08-31
- `0.1.2-alpha.2` -- 2026-08-30
- `0.1.1-rc.2` -- 2026-08-21
- `0.1.1-rc.1` -- 2026-08-21
- `0.1.0-rc.8` -- 2026-08-19
- `0.1.0-rc.7` -- 2026-08-17
- `0.1.0-rc.6` -- 2026-08-13
- `0.1.0-rc.3` -- 2026-08-13
- `0.1.0-rc.2` -- 2026-08-13
- `0.0.1-rc.5` -- 2026-08-12
- `0.0.1-rc.2` -- 2026-08-11
- `0.0.1-rc.1` -- 2026-08-10

The package publishes no readme; see the
[repository README](index.md) (github.com/deepseek-ai/deepseek-harness).
