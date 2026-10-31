---
title: "Context menu types and icons"
source: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/upgrade-guide/v0.2.2-alpha.2/context-menu-target/guide.md
fetched: 2026-10-31
---
# Context menu types and icons

English | [中文](guide.zh.md)

## Change

The `@deepseek-ai/dsh-client-ui-context-menu/client` export `MenuTarget` is renamed to `ContextMenuTarget`, matching `ContextMenuTargetMap`. The old name has no compatibility alias. Target fields and runtime behavior are unchanged. Workspace and sidebar injections rename `menuTarget` / `useMenuTarget` to `contextMenuTarget` / `useContextMenuTarget`. Action icons accept `{ key, src? }` instead of React nodes and render through the keyed `contextMenu.icon` Slot.

## Migration

1. Replace `MenuTarget` imports and type references with `ContextMenuTarget`.
2. Rename injected `menuTarget` sources and `useMenuTarget` consumers to `contextMenuTarget` and `useContextMenuTarget`.
3. Replace action icon elements with `{ key: 'my-plugin.action' }`; carry a captured image URL in `src` when needed. Register the icon component under that key through `ctx.slots.inject('contextMenu.icon', ...)` and `ctx.slots.register()`. See the [menu package](../../../../packages/client/ui-context-menu/README.md#use-this-package).
4. Rebuild custom Client plugins, confirm that type checks pass, and open their menus to verify icon rendering and plugin-unload cleanup.
