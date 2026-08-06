---
title: "Integrate with Reasonix"
description: "Reasonix is a coding agent that runs in the terminal."
source: https://api-docs.deepseek.com/quick_start/agent_integrations/reasonix
fetched: 2026-08-06
---

# Integrate with Reasonix

Reasonix is a coding agent that runs in the terminal.

#### 1. Install Node.js

- Install [Node.js](https://nodejs.org/en/download/) 20.10+.
- Windows users need to install [Git for Windows](https://git-scm.com/download/win).

#### 2. Get a DeepSeek API Key

Get your API Key from the [DeepSeek Platform](https://platform.deepseek.com/api_keys). The first run of Reasonix prompts for it via a built-in wizard and persists it to `~/.reasonix/config.json` — no environment variable needed.

#### 3. Enter the project directory and run `npx reasonix code` to get started.

```text
cd /path/to/my-project
npx reasonix code
```

No global install required. By default Reasonix uses **DeepSeek-V4-Flash** for cost-efficient iteration. Type `/pro` inside the TUI to arm **DeepSeek-V4-Pro** for the next turn, or `/preset max` to use Pro for the whole session. Run `/help` for the full slash-command reference.

![](https://raw.githubusercontent.com/esengine/reasonix/main/docs/logo.svg)
