---
title: "Integrate with Hermes Agent"
description: "Hermes is an open-source AI agent built by Nous Research."
source: https://api-docs.deepseek.com/quick_start/agent_integrations/hermes
fetched: 2026-08-08
---

# Integrate with Hermes Agent

Hermes is an open-source AI agent built by Nous Research.

#### 1. Install Hermes

##### Quick Install

Get Hermes Agent up and running in under two minutes with the one-line installer.

###### Linux / macOS / WSL2

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

The only prerequisite is Git. The installer automatically handles everything else.

For more installation instructions, please refer to the [Hermes installation page](https://hermes-agent.nousresearch.com/docs/getting-started/installation).

#### 2. Run and Configure

Reload your shell and start Hermes configuration:

- Execute the `hermes setup` command
- Choose the Quick Setup option
- When prompted for the model provider, select **DeepSeek**
- Enter your [DeepSeek API Key](https://platform.deepseek.com/api_keys)
- Enter the Base URL as `https://api.deepseek.com`
- Select the `deepseek-v4-pro` model
- Continue with the remaining options
