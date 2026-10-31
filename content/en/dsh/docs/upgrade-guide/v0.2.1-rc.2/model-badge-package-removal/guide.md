---
title: "The `ui-deepseek-model-label-1017` package is removed"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.1-rc.2/model-badge-package-removal/guide.md
fetched: 2026-10-31
---
# The `ui-deepseek-model-label-1017` package is removed

English | [中文](guide.zh.md)

## Change

`@deepseek-ai/dsh-client-ui-deepseek-model-label-1017` and its `ui-deepseek-model-label-1017` row in the Web bundle are removed, and the package receives no further releases. The composer model selector shows the badge that the DeepSeek `GET /models` listing declares for a model; without a declared badge, `DeepSeek-V4.1-Flash` shows no `1017`. A profile patch that disables or edits the removed row matches no entry, so boot warns that the entry is not found and skips the patch.

## Migration

1. Delete the patch whose `id` is `ui-deepseek-model-label-1017`, with its `disabled` or other fields, from `$DSH_HOME/profiles/<profile>/cordis.patch.yml` and from any overlay passed with `--patch`.
2. Remove `@deepseek-ai/dsh-client-ui-deepseek-model-label-1017` from the dependencies of any package that lists it.
3. To change how model names or badges render, contribute to the `conversation.input.model.label` slot; its owner props carry the catalog `model.badge` ([label extensions](../../../../packages/client/ui-model-selection/README.md#use-this-package)).
4. Restart DSH and confirm that boot reports no missing `ui-deepseek-model-label-1017` entry.
