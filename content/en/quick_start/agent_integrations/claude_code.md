---
title: "Integrate with Claude Code"
description: "Claude Code is an AI coding assistant that runs in the terminal."
source: https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code
fetched: 2026-08-02
---

# Integrate with Claude Code

Claude Code is an AI coding assistant that runs in the terminal.

## Migrate from Existing Installation to DeepSeek

If you already have Claude Code installed, simply configure the following environment variables to point to the [DeepSeek Anthropic API](https://api.deepseek.com/anthropic). Get your API Key from the [DeepSeek Platform](https://platform.deepseek.com/api_keys):

Linux / Mac users:

```text
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<your DeepSeek API Key>
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

Windows users:

```text
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

Then enter your project directory and run claude:

```text
cd /path/to/my-project
claude
```

## Install Claude Code from Scratch

#### 1. Install Claude Code

- Install [Node.js](https://nodejs.org/en/download/) 18+.
- Windows users need to install [Git for Windows](https://git-scm.com/download/win).
- Run the following command in your terminal to install Claude Code:

```text
npm install -g @anthropic-ai/claude-code
```

- After installation, run the following command. If the version number is displayed, the installation is successful:

```text
claude --version
```

#### 2. Configure Environment Variables

Linux / Mac users, run the following commands to configure the relevant environment variables. Get your API Key from the [DeepSeek Platform](https://platform.deepseek.com/api_keys):

```text
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<your DeepSeek API Key>
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

Windows users, run:

```text
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

#### 3. Enter the project directory and execute the `claude` command to get started.

```text
cd /path/to/my-project
claude
```

![](https://cdn.deepseek.com/api-docs/cc_example.png)

---

## Using Web Search in Claude Code

The DeepSeek API natively supports the Web Search feature in Claude Code. When using Claude Code, if the model determines that your question requires a web search, it will invoke the Web Search tool and perform the search through the API provided by DeepSeek. Because invoking the Web Search tool generates additional LLM API requests to summarize the retrieved search content, additional model token costs will be incurred.

The following image shows an example of triggering the Web Search feature in Claude Code, where the user's question (Help me to search for best Rust tutorials) triggered the Web Search tool:

![](https://api-docs.deepseek.com/img/cc_web_search_example.png)

---

## Model Mapping When Using Claude Code or Claude Desktop APP

When you use Claude Code or Claude Desktop APP, we map the Claude model names you pass in:

- Models starting with claude-opus are mapped to deepseek-v4-pro
- Models starting with claude-haiku or claude-sonnet are mapped to deepseek-v4-flash

With this mapping, when using the developer mode of the new Claude Desktop APP, you can bypass the APP's model name restrictions by simply changing the base\_url and api\_key to connect to DeepSeek models.
