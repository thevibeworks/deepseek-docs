---
title: "Forge viewer list rows no longer carry closing issues"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.3-alpha.2/forge-viewer-list-rows/guide.md
fetched: 2026-11-28
---
# Forge viewer list rows no longer carry closing issues

English | [中文](guide.zh.md)

## Change

`ChangeRequestSummary`, the row a `ForgeProvider` returns from `listForViewer`, loses `closingIssues` and `closingIssuesTruncated`. The Code review page no longer names the issues a listed change request closes; the change request's own overview still lists them from `ChangeRequestSnapshot.closingIssues`, which is unchanged. The GitHub provider's list search no longer reads closing issues.

This affects third-party `ForgeProvider` implementations that offer viewer lists and other code that builds or reads `ChangeRequestSummary` values. The type comes from `@deepseek-ai/dsh-experimental-forge`.

## Migration

1. In every `ChangeRequestSummary` a provider builds, remove `closingIssues` and `closingIssuesTruncated`, and drop the read that served only them.
2. In code that reads those fields from a list row, read `closingIssues` and `closingIssuesTruncated` of the change request's `ChangeRequestSnapshot` instead, which `ctx.forge.watch` delivers.
