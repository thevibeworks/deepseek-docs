---
title: "Token 用量计算"
description: "token 是模型用来表示自然语言文本的基本单位，也是我们的计费单元，可以直观的理解为“字”或“词”；通常 1 个中文词语、1 个英文单词、1 个数字或 1 个符号计为 1 个 token。"
source: https://api-docs.deepseek.com/zh-cn/quick_start/token_usage
fetched: 2026-08-29
---

# Token 用量计算

token 是模型用来表示自然语言文本的基本单位，也是我们的计费单元，可以直观的理解为“字”或“词”；通常 1 个中文词语、1 个英文单词、1 个数字或 1 个符号计为 1 个 token。

一般情况下模型中 token 和字数的换算比例大致如下：

- 1 个英文字符 ≈ 0.3 个 token。
- 1 个中文字符 ≈ 0.6 个 token。

但因为不同模型的分词不同，所以换算比例也存在差异，每一次实际处理 token 数量以模型返回为准，您可以从返回结果的 `usage` 中查看。

## 离线计算 Token 用量

您可以通过如下压缩包中的代码来运行 tokenizer，以离线计算一段文本的 Token 用量。

[deepseek\_tokenizer.zip](https://cdn.deepseek.com/api-docs/deepseek_v4_tokenizer.zip)

## 计算图片 Token 用量

您可以通过图片尺寸估算图片所占用的 token 数量。图片在进入模型前会被自动缩放，每张图片消耗的 token 数存在上限，详见[图像理解](../guides/vision.md#token-usage)。

此处为估算值，实际处理时转换得到的 token 数量可能存在一定误差，请以接口返回的用量为准。

#### 图片 Token 计算器

宽度 (px)

高度 (px)
