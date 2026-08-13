---
title: "Models & Pricing"
description: "The prices listed below are in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We will bill based on the total number of input and output tokens by the model."
source: https://api-docs.deepseek.com/quick_start/pricing
fetched: 2026-08-13
---

# Models & Pricing

The prices listed below are in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We will bill based on the total number of input and output tokens by the model.

---

## Model Details

|  |  |  |  |
| --- | --- | --- | --- |
| MODEL | | deepseek-v4-flash | deepseek-v4-pro |
| BASE URL (OpenAI Format) | | <https://api.deepseek.com> | |
| BASE URL (Anthropic Format) | | <https://api.deepseek.com/anthropic> | |
| MODEL VERSION | | DeepSeek-V4-Flash-0731 | DeepSeek-V4-Pro-0813 |
| THINKING MODE | | Supports both non-thinking and thinking (default) modes See [Thinking Mode](../guides/thinking_mode.md) for how to switch | |
| CONTEXT LENGTH | | 1M | |
| MAX OUTPUT | | MAXIMUM: 384K | |
| FEATURES | [Json Output](../guides/json_mode.md) | ✓ | ✓ |
| [Tool Calls](../guides/tool_calls.md) | ✓ | ✓ |
| [Responses API](../guides/responses_api.md) | ✓ | ✓ |
| [Anthropic API](../guides/anthropic_api.md) | ✓ | ✓ |
| [Chat Prefix Completion（Beta）](../guides/chat_prefix_completion.md) | ✓ | ✓ |
| [FIM Completion（Beta）](../guides/fim_completion.md) | Non-thinking mode only | Non-thinking mode only |
| PRICING(1) | 1M INPUT TOKENS (CACHE HIT) | $0.0028 | $0.003625 |
| 1M INPUT TOKENS (CACHE MISS) | $0.14 | $0.435 |
| 1M OUTPUT TOKENS | $0.28 | $0.87 |
| Concurrency Limit(2) | | 2500 | 500 |

(1) DeepSeek API pricing will be updated to peak / off-peak billing, with off-peak rates at half the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC (all other hours are off-peak). The new prices take effect at 16:00 UTC on August 16, 2026, as follows:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| MODEL | | 1M INPUT TOKENS (CACHE HIT) | 1M INPUT TOKENS (CACHE MISS) | 1M OUTPUT TOKENS |
| deepseek-v4-flash | OFF-PEAK | $0.007 | $0.22 | $0.66 |
| PEAK | $0.014 | $0.44 | $1.32 |
| deepseek-v4-pro | OFF-PEAK | $0.022 | $0.66 | $1.98 |
| PEAK | $0.044 | $1.32 | $3.96 |

(2) For more details on concurrency limits, please refer to [Rate Limit & Isolation](rate_limit.md)

---

## Deduction Rules

The expense = number of tokens × price.
The corresponding fees will be directly deducted from your topped-up balance or granted balance, with a preference for using the granted balance first when both balances are available.

Product prices may vary and DeepSeek reserves the right to adjust them. We recommend topping up based on your actual usage and regularly checking this page for the most recent pricing information.
