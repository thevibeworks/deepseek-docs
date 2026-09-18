---
title: "Integrate with Qoder"
description: "Qoder is an agentic coding product available in three forms: IDE, CLI, and JetBrains Plugin."
source: https://api-docs.deepseek.com/quick_start/agent_integrations/qoder
fetched: 2026-09-18
---

# Integrate with Qoder

Qoder is an agentic coding product available in three forms: IDE, CLI, and JetBrains Plugin.

> Two ways to use DeepSeek — pick either one:
>
> - **Built-in models**: no extra configuration is needed — just pick one from the model selector. Usage is billed uniformly with Qoder Credits.
> - **Custom models**: connect with your DeepSeek API key. Available in the Personal edition; usage is billed directly to your DeepSeek API account and does not consume Qoder Credits. This guide covers this approach.

## Installing Qoder from Scratch

Qoder can be used via IDE, CLI, or JetBrains Plugin. Choose whichever you prefer.

### Option 1: Install Qoder IDE

- Download and install Qoder IDE from the [official website](https://qoder.com/ide), available for macOS, Windows, and Linux.
- Launch Qoder IDE and sign in with your account.

### Option 2: Install Qoder CLI

- macOS / Linux users, run the following command in your terminal:

```text
curl -fsSL https://qoder.com/install | bash
```

- Windows users, run in PowerShell:

```text
irm https://qoder.com/install.ps1 | iex
```

- If you already have [Node.js](https://nodejs.org/en/download/) 20+, you can also install globally via npm:

```text
npm install -g @qoder-ai/qodercli
```

- After installation, run the following command. If the version number is displayed, the installation is successful:

```text
qodercli --version
```

### Option 3: Install Qoder JetBrains Plugin

- Prepare a JetBrains IDE of version 2020.3 or later.
- Open the Settings of your JetBrains IDE (`⌘ ,` on macOS, `Ctrl+Alt+S` on Windows / Linux) and go to `Plugins`.
- Search for `Qoder`, click `Install`, and restart the IDE after installation.
- Click the Qoder icon in the right-side navigation bar and click `Sign in` to sign in with your account.

## Configuring Qoder

Before configuring a custom model, get your API key from the [DeepSeek Platform](https://platform.deepseek.com/api_keys).

### Configuring Qoder IDE

1. **Open Qoder IDE Settings**: click `Qoder IDE` in the top-left corner of the IDE, then select `Settings` -> `Qoder IDE Settings` to open the settings panel.
2. **Open the Models panel**: select `Models` in the left navigation bar.
3. **Add a model**: click `+ Add`, select **DeepSeek** as the provider, choose the model you need (e.g. DeepSeek-V4-Pro or DeepSeek-V4-Flash), and fill in your API key.
4. **Verify the connection**: click `Add`, and the connection will be verified automatically.

### Configuring Qoder CLI

1. Type `/model` in the CLI and switch to the **Custom** tab.
2. Select `Add custom model...` and follow the wizard to choose Provider (DeepSeek) → model type → specific model.
3. Fill in your API key. Once verified, the configuration is saved automatically and the model is ready to use.

> Configure custom models via the Custom wizard in `/model`. Do not configure them manually in `settings.json`.

### Configuring Qoder JetBrains Plugin

1. Open the settings in the top-right corner of the Qoder panel and select `Plugin Settings`.
2. Select `Add Model`, pick **DeepSeek** as the provider, and fill in your API key.

## Using Qoder

DeepSeek V4 models support up to **1M tokens of context** and the **max thinking effort level**. After selecting a model, you can set its context window and thinking effort in the model selector.

### Using Qoder IDE

Open your project in Qoder IDE, select the DeepSeek model you just added from the model selector in the chat input box, and start coding.

### Using Qoder CLI

Enter the project directory and execute the `qodercli` command; then type `/model` to open the model selector, switch to the **Custom** tab, and select the DeepSeek model you added.

```text
cd /path/to/my-project
qodercli
```

### Using Qoder JetBrains Plugin

Open your project in a JetBrains IDE, click the Qoder icon in the right-side navigation bar (or press `⌘ ⇧ L` / `Ctrl+Shift+L`) to open the Chat panel, and select the configured DeepSeek model from the model selector to get started.

For more details, see the [Qoder custom models documentation](https://docs.qoder.com/user-guide/chat/custom-models) and the [Qoder CLI custom models documentation](https://docs.qoder.com/cli/custom-models).

## Troubleshooting

- Adding the model fails: Check whether the API key is correct with no extra spaces, and confirm it has not expired or been disabled.
- Connection verification fails or requests error out: Check whether your DeepSeek account has sufficient balance and your network connection is working.
