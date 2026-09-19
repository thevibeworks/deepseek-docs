---
title: "Models & Pricing"
description: "The prices listed below are in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We will bill based on the total number of input and output tokens by the model."
source: https://api-docs.deepseek.com/quick_start/pricing
fetched: 2026-09-19
---

# Models & Pricing

The prices listed below are in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We will bill based on the total number of input and output tokens by the model.

---

## Model Details

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| MODEL | | | deepseek-flash(1) | deepseek-v4-pro |
| BASE URL (OpenAI Format) | | | <https://api.deepseek.com> | |
| BASE URL (Anthropic Format) | | | <https://api.deepseek.com/anthropic> | |
| MODEL VERSION | | | DeepSeek-V4.1-Flash | DeepSeek-V4-Pro-0813 |
| THINKING MODE | | | Supports both non-thinking and thinking (default) modes See [Thinking Mode](../guides/thinking_mode.md) for how to switch | |
| CONTEXT LENGTH | | | 1M | |
| MAX OUTPUT | | | MAXIMUM: 384K | |
| FEATURES | [Json Output](../guides/json_mode.md) | | ✓ | ✓ |
| [Tool Calls](../guides/tool_calls.md) | | ✓ | ✓ |
| [Responses API](../guides/responses_api.md) | | ✓ | ✓ |
| [Anthropic API](../guides/anthropic_api.md) | | ✓ | ✓ |
| [Chat Prefix Completion（Beta）](../guides/chat_prefix_completion.md) | | ✓ | ✓ |
| [FIM Completion（Beta）](../guides/fim_completion.md) | | Non-thinking mode only | Non-thinking mode only |
| [Vision](../guides/vision.md) | | ✓ | Not supported |
| PRICING(2) | 1M INPUT TOKENS (CACHE HIT) | OFF-PEAK | $0.003 | $0.022 |
| PEAK | $0.006 | $0.044 |
| 1M INPUT TOKENS (CACHE MISS) | OFF-PEAK | $0.15 | $0.66 |
| PEAK | $0.3 | $1.32 |
| 1M OUTPUT TOKENS | OFF-PEAK | $0.6 | $1.98 |
| PEAK | $1.2 | $3.96 |
| Concurrency Limit(3) | | | 2500 | 500 |

(1) Use `deepseek-flash` as the model name. The legacy names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are still accepted, but the corresponding models have been retired, their requests are served by the DeepSeek-V4.1-Flash model and billed at the Flash price.

(2) Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays. All other hours are off-peak, including weekends and Chinese public holidays in full.

(3) For more details on concurrency limits, please refer to [Rate Limit & Isolation](rate_limit.md).

---

## Deduction Rules

The expense = number of tokens × price.
The corresponding fees will be directly deducted from your topped-up balance or granted balance, with a preference for using the granted balance first when both balances are available.

Product prices may vary and DeepSeek reserves the right to adjust them. We recommend topping up based on your actual usage and regularly checking this page for the most recent pricing information.
