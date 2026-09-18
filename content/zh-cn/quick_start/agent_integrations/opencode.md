---
title: "接入 OpenCode"
description: "OpenCode 是一个开源 AI 编程助手，提供终端、网页等运行形式。"
source: https://api-docs.deepseek.com/zh-cn/quick_start/agent_integrations/opencode
fetched: 2026-09-18
---

# 接入 OpenCode

OpenCode 是一个开源 AI 编程助手，提供终端、网页等运行形式。

## 从现有安装中迁移到 DeepSeek

1. 执行 `opencode upgrade` 命令，将 opencode 升级至最新版本（>=v1.18.30）
2. 执行 `opencode` 命令，启动 OpenCode
3. 输入框中输入 `/connect`，然后输入 `deepseek` 并选择供应商

![](https://api-docs.deepseek.com/zh-cn/img/opencode_1.png)

![](https://api-docs.deepseek.com/zh-cn/img/opencode_2.png)

3. 填入 [DeepSeek API Key](https://platform.deepseek.com/api_keys)

![](https://api-docs.deepseek.com/zh-cn/img/opencode_3.png)

4. 选择 DeepSeek-V4-Flash 模型

![](https://api-docs.deepseek.com/zh-cn/img/opencode_4.png)

---

## 从零安装 OpenCode

#### 1. 安装 OpenCode

前往官方下载页面安装或升级：[OpenCode 下载](https://opencode.ai/zh/download)

为避免兼容性问题，强烈建议您将 OpenCode 升级到最新版本，确保版本号 >= v1.18.30。

#### 2. 运行与配置

- 执行 `opencode` 命令
- 输入框中输入 `/connect`，然后输入 `deepseek` 并选择供应商
- 填入 [DeepSeek API Key](https://platform.deepseek.com/api_keys)
- 选择 DeepSeek-V4-Flash 模型
