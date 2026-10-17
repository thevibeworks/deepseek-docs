---
title: "Models & Pricing"
description: "Model prices are listed in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We bill model usage based on the total number of input and output tokens by the model."
source: https://api-docs.deepseek.com/quick_start/pricing
fetched: 2026-10-17
---

# Models & Pricing

Model prices are listed in units of per 1M tokens. A token, the smallest unit of text that the model recognizes, can be a word, a number, or even a punctuation mark. We bill model usage based on the total number of input and output tokens by the model.

---

## Model Details

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| MODEL | | | deepseek-flash(1) | deepseek-v4-pro |
| BASE URL (OpenAI Format) | | | <https://api.deepseek.com> | |
| BASE URL (Anthropic Format) | | | <https://api.deepseek.com/anthropic> | |
| MODEL VERSION | | | DeepSeek-V4.1-Flash-1017 | DeepSeek-V4-Pro-0813 |
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

(1) Use `deepseek-flash` as the model name. The legacy names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are still accepted, but the corresponding models have been retired, their requests are served by the DeepSeek-V4.1-Flash-1017 model and billed at the Flash price.

(2) Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays. All other hours are off-peak, including weekends and Chinese public holidays in full.

(3) For more details on concurrency limits, please refer to [Rate Limit & Isolation](rate_limit.md).

---

## Search & Fetch Pricing

Search and Fetch are standalone APIs billed per request.

| API | Unit | Price |
| --- | --- | --- |
| Search | Per 1,000 successful requests | $0.75 |
| Fetch | Per 1,000 successful requests | $0.75 |

Note: when you use the DeepSeek API through DeepSeek Harness, Claude Code, or Codex, server-side tool calls already hit the Search and Fetch APIs. These calls are currently free of charge; per-request billing starts at 00:00 Beijing time on November 1, 2026.

See the [Search & Fetch guide](../guides/search.md) for API usage and complete billing rules.

---

## Deduction Rules

For model usage, the expense = number of tokens × price. Search and Fetch are charged per successful request at the rates above.
The corresponding fees will be directly deducted from your topped-up balance or granted balance, with a preference for using the granted balance first when both balances are available.

Product prices may vary and DeepSeek reserves the right to adjust them. We recommend topping up based on your actual usage and regularly checking this page for the most recent pricing information.
