---
title: "接入 Qoder"
description: "Qoder 是一款 Agentic Coding 产品，支持 IDE、CLI 和 JetBrains Plugin 三种形态。"
source: https://api-docs.deepseek.com/zh-cn/quick_start/agent_integrations/qoder
fetched: 2026-09-18
---

# 接入 Qoder

Qoder 是一款 Agentic Coding 产品，支持 IDE、CLI 和 JetBrains Plugin 三种形态。

> 两种接入方式任选其一：
>
> - **内置模型**：无需额外配置，在模型选择器中直接选用即可，统一使用 Qoder Credits 计费。
> - **自定义模型**：通过 DeepSeek API 密钥接入，适用于个人版，费用由 DeepSeek API 账户直接结算，不占用 Qoder Credits。本指南介绍这种方式的配置步骤。

## 从零安装 Qoder

Qoder 可以通过 IDE、CLI 或 JetBrains Plugin 的方式运行，按照使用习惯任选即可。

### 选项一：安装 Qoder IDE

- 前往 [Qoder IDE 官网](https://qoder.com/zh/ide) 下载并安装，支持 macOS、Windows 与 Linux。
- 启动 Qoder IDE 并登录账号。

### 选项二：安装 Qoder CLI

- macOS / Linux 用户，在命令行界面执行以下命令安装：

```text
curl -fsSL https://qoder.com/install | bash
```

- Windows 用户，在 PowerShell 中执行：

```text
irm https://qoder.com/install.ps1 | iex
```

- 已安装 [Node.js](https://nodejs.org/zh-cn/download/) 20+ 的用户，也可以通过 npm 全局安装：

```text
npm install -g @qoder-ai/qodercli
```

- 安装结束后，执行以下命令，若显示版本号则安装成功：

```text
qodercli --version
```

### 选项三：安装 Qoder JetBrains Plugin

- 准备一个 2020.3 或更高版本的 JetBrains IDE。
- 打开 JetBrains IDE 的 Settings（macOS 按 `⌘ ,`，Windows / Linux 按 `Ctrl+Alt+S`），进入 `Plugins`。
- 搜索 `Qoder` 并点击 `Install` 安装，安装完成后重启 IDE。
- 点击右侧导航栏的 Qoder 图标，点击 `Sign in` 登录账号。

## 配置 Qoder

配置自定义模型前，先在 [DeepSeek 开放平台](https://platform.deepseek.com/api_keys) 获取 API 密钥。

### 配置 Qoder IDE

1. **进入 Qoder IDE 设置**：点击 IDE 左上角的 `Qoder IDE`，选择 `设置` -> `Qoder IDE 设置`，打开设置面板。
2. **进入模型面板**：在左侧导航栏中选择「模型」。
3. **添加模型**：点击「+ 添加」，服务商选择 **DeepSeek**，按需选择所需模型（如 DeepSeek-V4-Pro 或 DeepSeek-V4-Flash），并填写你的 API 密钥。
4. **验证连接**：点击「添加」，系统将自动验证连接状态。

### 配置 Qoder CLI

1. 在 CLI 中输入 `/model`，切换到 **Custom** 页签。
2. 选择 `Add custom model...`，按向导依次选择 Provider（DeepSeek）→ 模型类型 → 具体模型。
3. 填写 API 密钥，验证通过后配置自动保存，可立即切换使用。

> 请通过 `/model` 的 Custom 向导配置自定义模型，不要在 `settings.json` 中手工配置。

### 配置 Qoder JetBrains Plugin

1. 在 Qoder 面板右上角打开设置，选择「插件设置」。
2. 选择「添加模型」，服务商选择 **DeepSeek** 并填写 API 密钥即可。

## 使用 Qoder

DeepSeek V4 系列模型支持最高 **1M 上下文**与 **max 级别思考强度**。选定模型后，可在模型选择器中为其设置上下文窗口与思考强度。

### 使用 Qoder IDE

用 Qoder IDE 打开项目，在对话输入框的模型选择器中选择刚添加的 DeepSeek 模型，即可开始使用。

### 使用 Qoder CLI

进入项目目录，执行 `qodercli` 命令；输入 `/model` 打开模型选择器，切换到 **Custom** 页签选中已添加的 DeepSeek 模型，即可开始使用。

```text
cd /path/to/my-project
qodercli
```

### 使用 Qoder JetBrains Plugin

用 JetBrains IDE 打开项目，点击右侧导航栏的 Qoder 图标（或按 `⌘ ⇧ L` / `Ctrl+Shift+L`）打开 Chat 面板，在模型选择器中选择已配置的 DeepSeek 模型，即可开始使用。

更多细节请参阅 [Qoder 自定义模型文档](https://docs.qoder.com/zh/user-guide/chat/custom-models) 与 [Qoder CLI 自定义模型文档](https://docs.qoder.com/zh/cli/custom-models)。

## 常见问题

- 添加模型失败：检查 API 密钥是否正确，无多余空格；确认密钥未过期或被禁用。
- 验证连接不通过或调用报错：检查 DeepSeek 账户余额是否充足，网络连接是否正常。
