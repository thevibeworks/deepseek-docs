---
title: "更新日志"
description: "时间: 2026-09-10"
source: https://api-docs.deepseek.com/zh-cn/updates
fetched: 2026-09-18
---

# 更新日志

---

## 时间: 2026-09-10

### DeepSeek-V4.1-Flash 发布

今天，我们正式发布 DeepSeek-V4.1-Flash 模型。这是我们全新模型结构系列中的最小尺寸的模型，具备原生多模态视觉理解能力。新模型结构的设计初衷是：能力上限更高、推理速度更快、吞吐更大、可扩展到更大参数模型。

- GPQA Diamond: 90.9
- HLE: 36.8 (39.1\*)
- Codeforces (Rating): 3471
- MathArena Apex: 65.6
- Terminal-Bench 2.1: 90.6
- Terminal-Bench 3.0: 30.0
- Terminal-Bench 4.0: 31.2
- DeepSWE v1.1: 74.2
- ProgramBench: 20.3
- NL2Repo-Bench: 65.4
- CyberGym: 88.1
- SEC-Bench Pro: 62.8
- ExploitGym: 15.3
- HLE (w/tools): 63.9
- Automation-Bench: 54.8
- Agents' Last Exam: 31.8
- Chartography (w/tools): 78.9
- BabyVision (w/tools): 89.6
- ZeroBench-main (w/tools): 49.0

\* 表示仅在 HLE 评测集的纯文本子集上进行了测试。

**API 变更**

DeepSeek V4.1 Flash 已同步上线 DeepSeek API，原生支持多模态，将模型名称更改为 `deepseek-flash` 即可调用最新的 V4.1 Flash 模型。旧版本模型 V4 Flash 与 V4 Flash Vision Exp 现已下线，出于兼容考虑，模型名 `deepseek-v4-flash`、`deepseek-v4-flash-vision-exp` 将被暂时路由到 V4.1 Flash。

为响应广大用户的需求，我们决定在 2026 年 9 月 14 日之后继续提供 DeepSeek V4 Pro 的 API 调用服务，计费方式保持不变；如有变动，我们将另行通知。感谢您的理解与支持！

**API 定价调整**

随着 DeepSeek-V4.1-Flash 上线，API 价格同步下调。详细价格请参考[模型与价格](quick_start/pricing.md)。

详细更新内容请[参阅文档](news/news260910.md)。

---

## 时间: 2026-08-21

### DeepSeek-V4-Flash-Vision-Exp 发布

今天，全新的多模态视觉理解模型 DeepSeek-V4-Flash-Vision-Exp 上线 DeepSeek API 平台，这是一个实验性质的模型，用户可以通过设置 model='deepseek-v4-flash-vision-exp' 访问该模型。

- Terminal Bench 2.1: 83.9
- NL2Repo: 57.7
- DeepSWE: 59.3
- DSBench-Hard: 63.6
- AutomationBench (Public): 25.7
- ApexBench (Pass@1): 36.5
- Agents' Last Exam: 27.3
- Chartography: 64.3
- ZeroBench (Pass@5): 35.0

\* 对于公开基准测试集中的 Code Agent 文本任务，DeepSeek 系列模型使用 DeepSeek Harness 极简模式作为框架进行测试，并使用 max 档位，topp=0.95，temperature=1.0；在 ApexBench 与 Agents' Last Exam 测评中，文本模型 DeepSeek-V4-Flash 会忽略其中的多模态元素

在纯文本能力（Agent、推理、世界知识等）方面，DeepSeek-V4-Flash-Vision-Exp 与 DeepSeek-V4-Flash 正式版持平。

在需要视觉理解的 Agent Benchmark 上，DeepSeek-V4-Flash-Vision-Exp 相比 DeepSeek-V4-Flash 实现了大幅跃升，多模态 Agent 能力已接近 Opus-4.8。

详细调用方法请[参阅文档](guides/vision.md)。

---

## 时间: 2026-08-13

### DeepSeek-V4-Pro 更新

DeepSeek-V4-Pro 正式版已同步在 APP、网页端和 API 更新上线。API 调用方式不变，模型名设置为 `deepseek-v4-pro`，即可使用最新版本。

**Agent 能力大幅提升**

正式版 DeepSeek V4 Pro 极大增强了 Agent 能力，在生产环境中的性能表现提升尤为显著。

- HLE (wo / w tools): 42.7/60.0
- Terminal Bench 2.1: 87.9
- NL2Repo: 61.5
- Cybergym: 83.3
- DeepSWE: 62.7
- Toolathlon-Verified: 74.1
- Agents' Last Exam: 25.7
- AutomationBench (Public): 31.8
- DSBench-FullStack: 71.1
- DSBench-Hard: 67.2

**原生支持 Responses API**

DeepSeek API 现已原生支持 OpenAI Responses API 格式，并针对性适配 Codex。用户可以参考[官方文档](quick_start/agent_integrations/codex.md)，通过一键配置脚本完成 Codex 的配置。

**更灵活的思考强度控制**

V4-Pro 和 V4-Flash 思考模式现支持 low / high / max 三档思考强度，用户在实际使用中可以根据任务复杂度灵活选择：简单任务使用 low，日常 Agent 任务使用 high，更复杂的任务场景使用 max。设置方法请参考官方 API 文档：[思考模式](guides/thinking_mode.md)。

**API 定价调整**

随着 DeepSeek V4 全系列模型正式版上线，我们将对 API 价格进行[更新调整](quick_start/pricing.md)。为了更加合理地调配资源，我们将采用峰谷定价，闲时价格为高峰时段价格的一半，鼓励用户根据实际使用情况调整任务时间。新价格将于北京时间 2026 年 8 月 17 日 0 时开始生效。

详细更新内容请[参阅文档](news/news260813.md)

---

## 时间: 2026-07-31

### DeepSeek-V4-Flash 更新

DeepSeek-V4-Flash 正式版 API 上线公测，API 调用方式不变，模型名设置为 `deepseek-v4-flash` 即可使用最新版本。

**Agent 能力大幅增强，基准测试远超 V4-Pro-Preview：**

- Terminal Bench 2.1: 82.7
- NL2Repo: 54.2
- Cybergym: 76.7
- DeepSWE: 54.4
- Toolathlon verified: 70.3
- Agent Last Exam: 25.2
- Automation Bench (Public): 25.1
- DSBench-FullStack: 68.7
- DSBench-Hard: 59.6

注1：对于公开基准测试集中的 Code Agent 任务，正式版 DeepSeek-V4-Flash 使用 DeepSeek Harness 极简模式（即将发布）作为框架进行测试，并使用 max 档位，topp=0.95，temperature=1.0
注2：DSBench-FullStack 是内部使用的全栈开发测试集，DSBench-Hard 是内部使用的 Coding Agent 难题测试集

**正式版 V4-Flash 原生支持 Responses API 格式并针对性适配 Codex，具体配置方法请参考[文档](quick_start/agent_integrations/codex.md)**

**DeepSeek-V4-Flash-0731 的模型结构、尺寸和 DeepSeek-V4-Flash-Preview 保持一致，仅重新进行了后训练。**

**注意：本次仅升级了 DeepSeek-V4-Flash 的 API 接口，DeepSeek-V4-Pro API 及 APP/WEB 端模型未做更改。**

**DeepSeek-V4-Pro 正式版将会尽快发布。**

---

## 时间: 2026-04-24

### DeepSeek-V4

DeepSeek API 已支持 V4-Pro 与 V4-Flash，支持 OpenAI ChatCompletions 接口与 Anthropic 接口。访问新模型时，base\_url 不变, model 参数需要改为 `deepseek-v4-pro` 或 `deepseek-v4-flash`。

旧有的 API 接口的两个模型名 `deepseek-chat` 与 `deepseek-reasoner` 将于三个月后（2026-07-24）停止使用。当前阶段内，这两个模型名分别指向 `deepseek-v4-flash` 的非思考模式与思考模式。

详细更新内容请[参阅文档](news/news260424.md)

---

## 时间: 2025-12-01

### DeepSeek-V3.2

`deepseek-chat` 和 `deepseek-reasoner` 都已升级为 DeepSeek-V3.2.

- `deepseek-chat` 对应 DeepSeek-V3.2 的**非思考模式**
- `deepseek-reasoner` 对应 DeepSeek-V3.2 的**思考模式**

### DeepSeek-V3.2-Speciale

我们非正式部署了 DeepSeek-V3.2-Speciale 的 API 服务，API 用户可以通过设置 `base_url="https://api.deepseek.com/v3.2_speciale_expires_on_20251215"` 访问该模型。该模型 API 价格不变，只支持思考模式下的对话功能，不支持工具调用等功能，最大输出长度默认为 128K，支持时间截止至北京时间 2025-12-15 23:59。

详细更新内容请[参阅文档](news/news251201.md)

---

## 时间: 2025-09-29

### DeepSeek-V3.2-Exp

`deepseek-chat` 和 `deepseek-reasoner` 都已经升级为 DeepSeek-V3.2-Exp。

- `deepseek-chat` 对应 DeepSeek-V3.2-Exp 的**非思考模式**
- `deepseek-reasoner` 对应 DeepSeek-V3.2-Exp 的**思考模式**

详细更新内容请[参阅文档](news/news250929.md)

---

## 时间: 2025-09-22

### DeepSeek-V3.1-Terminus

**`deepseek-chat` 和 `deepseek-reasoner` 都已经升级为 DeepSeek-V3.1-Terminus。**`deepseek-chat` 对应 DeepSeek-V3.1-Terminus 的**非思考模式**，`deepseek-reasoner` 对应 DeepSeek-V3.1-Terminus 的**思考模式**。

此次更新在保持模型原有能力的基础上，针对用户反馈的问题进行了改进，包括：

- 语言一致性：缓解了中英文混杂、偶发异常字符等情况；
- Agent能力：进一步优化了 Code Agent 与 Search Agent 的表现。

---

## 时间: 2025-08-21

### DeepSeek-V3.1

**`deepseek-chat` 和 `deepseek-reasoner` 都已经升级为 DeepSeek-V3.1。**`deepseek-chat` 对应 DeepSeek-V3.1 的**非思考模式**，`deepseek-reasoner` 对应 DeepSeek-V3.1 的**思考模式**。

- DeepSeek-V3.1 包含以下主要变化：
  - 混合推理架构：一个模型同时支持思考模式与非思考模式
  - 更高的思考效率：相比 DeepSeek-R1-0528，DeepSeek-V3.1-Think 能在更短时间内给出答案
  - 更强的 Agent 能力：通过 Post-Training 优化，新模型在工具使用与智能体任务中的表现有较大提升
    - SWE-bench Verified: 66.0
    - SWE-bench Multilingual: 54.5
    - Terminal-bench: 31.3

---

## 时间: 2025-05-28

### deepseek-reasoner

**`deepseek-reasoner` 模型升级为 DeepSeek-R1-0528：**

- **推理能力增强**
  - 基准测试提升显著（Pass@1）
    - AIME 2025: 70.0→ 87.5 (+17.5)
    - GPQA: 71.5 → 81.0 (+9.5)
    - LCB\_v6: 63.5 → 73.3 (+9.8)
    - Aider: 57.0 → 71.6 (+14.6)
  - 注：复杂推理问题相比老版本R1会使用更多tokens
- **Web前端开发能力优化**
  - 生成的网页与游戏更加美观
- **幻觉降低**
  - 极大程度抑制了老版本R1所存在的幻觉问题
- **Json Output与Function Calling 支持**
  - Function call性能
    - Tau-bench score: 53.5 (Airline)/63.9 (Retail)

---

## 时间: 2025-03-24

### deepseek-chat

**`deepseek-chat` 模型升级为 DeepSeek-V3-0324：**

- **推理能力增强**
  - 基准测试提升显著
    - MMLU-Pro: 75.9 → 81.2 (+5.3)
    - GPQA: 59.1 → 68.4 (+9.3)
    - AIME: 39.6 → 59.4 (+19.8)
    - LiveCodeBench: 39.2 → 49.2 (+10.0)
- **Web前端开发能力优化**
  - 代码生成准确率提升
  - 生成的网页与游戏前端更加美观
- **中文写作能力升级**
  - 风格与内容优化
    - 实现与R1写作风格对齐
    - 中长篇写作内容质量提升
- **功能增强**
  - 多轮交互式改写能力提升
  - 翻译质量与书信写作优化
- **中文搜索能力优化**
  - 报告分析类请求优化，输出内容详实
- **Function Calling 能力改进**
  - Function Calling 准确率提升，修复 V3 之前的问题

---

## 时间: 2025-01-20

### deepseek-reasoner

- `deepseek-reasoner` 是我们的新模型 DeepSeek-R1. 可以通过指定 `model=deepseek-reasoner` 调用。
- 详细更新，请参考: [DeepSeek-R1 正式发布](news/news250120.md)
- 调用指南，请参考: [推理模型](guides/thinking_mode.md)

---

## 时间: 2024-12-26

### deepseek-chat

- `deepseek-chat` 模型升级为 DeepSeek-V3，接口不变，可以通过指定 `model=deepseek-chat` 调用。
- 详细更新，请参考：[DeepSeek-V3 正式发布](news/news1226.md)

---

## 时间：2024-12-10

### deepseek-chat

deepseek-chat 模型升级为 DeepSeek-V2.5-1210，模型各项能力提升，相关基准测试：

- 数学能力：在 MATH-500 基准测试中的表现从 74.8% 提升至 82.8%
- 代码能力：在 LiveCodebench (08.01 - 12.01) 基准测试中的准确率从 29.2% 提升至 34.38%
- 中文写作与推理能力：在内部测试集中表现也有相应提升

与此同时，全新版本的模型对文件上传和网页总结功能的用户体验进行了优化。

---

## 时间：2024-09-05

### `deepseek-coder` & `deepseek-chat` 升级为 DeepSeek V2.5 模型

DeepSeek V2 Chat 和 DeepSeek Coder V2 两个模型已经合并升级，升级后的新模型为 DeepSeek V2.5。

为向前兼容，API 用户通过 `deepseek-coder` 或 `deepseek-chat` 均可以访问新的模型。

新模型在通用能力、代码能力上，都显著超过了旧版本的两个模型。

**新模型更好的对齐了人类的偏好，在写作任务、指令跟随等多方面进行了优化：**

- ArenaHard winrate从 68.3% 提升至 76.3%
- AlpacaEval 2.0 LC winrate从 46.61% 提升至 50.52%
- MT-Bench 分数从 8.84 提升至 9.02
- AlignBench 分数从 7.88 提升至 8.04

**新模型在原Coder模型的基础上进一步提升了代码生成能力，对常见编程应用场景进行了优化，并在标准测试集上取得了以下成绩：**

- HumanEval: 89%
- LiveCodeBench (1-9月): 41%

---

## 时间：2024-08-02

### API 上线硬盘缓存技术

DeepSeek API 创新采用硬盘缓存，价格再降一个数量级

更新详情请跳转文档 [API 上线硬盘缓存 2024/08/02](news/news0802.md)

---

## 时间：2024-07-25

### API 接口更新

- **更新接口 `/chat/completions`**
  - JSON 输出
  - Function 调用
  - 对话前缀续写（Beta）
  - 8K 最长输出（Beta）
- **新增接口 `/completions`**
  - FIM 补全（Beta）

更新详情请跳转文档 [API 升级新功能 2024/07/25](news/news0725.md)

---

## 时间：2024-07-24

### deepseek-coder

deepseek-coder 模型升级为 DeepSeek-Coder-V2-0724。

---

## 时间：2024-06-28

### deepseek-chat

`deepseek-chat` 模型升级为 DeepSeek-V2-0628，模型推理能力提升，相关基准测试：

- 代码，HumanEval Pass@1 79.88% -> 84.76%
- 数学，MATH ACC@1 55.02% -> 71.02%
- 推理，BBH 78.56% -> 83.40%

在 Arena-Hard 测评中，与 GPT-4-0314 的对战胜率从 41.6% 提升到了 68.3%。

模型角色扮演能力显著增强，可以在对话中按要求扮演不同角色。

---

## 时间：2024-06-14

### deepseek-coder

`deepseek-coder` 模型升级为 DeepSeek-Coder-V2-0614，代码能力显著提升，在代码生成、代码理解、代码修复和代码补全上达到了 GPT-4-Turbo-0409 的水平，并拥有卓越的数学和推理能力，其通用能力与 DeepSeek-V2-0517 持平。

---

## 时间：2024-05-17

### deepseek-chat

`deepseek-chat` 模型升级为 DeepSeek-V2-0517，模型在指令跟随方面的性能得到了显著提升，IFEval Benchmark Prompt-Level 准确率从 63.9% 跃升至 77.6%。此外，我们对API端的“system”区域指令跟随能力进行了优化，显著增强了沉浸式翻译、RAG 等任务的用户体验。

模型对于 JSON 格式输出的准确性得到了提升。在内部测试集中，JSON 解析率从 78% 提高到了85%。通过引入恰当的正则表达式，JSON 解析率进一步提高至 97%。
