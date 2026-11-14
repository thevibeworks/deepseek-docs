---
title: "Error Codes"
description: "When calling DeepSeek API, you may encounter errors. Here list the causes and solutions."
source: https://api-docs.deepseek.com/quick_start/error_codes
fetched: 2026-11-14
---

# Error Codes

When calling DeepSeek API, you may encounter errors. Here list the causes and solutions.

| CODE | DESCRIPTION |
| --- | --- |
| 400 - Invalid Format | **Cause**: Invalid request body format.   **Solution**: Please modify your request body according to the hints in the error message. For more API format details, please refer to [DeepSeek API Docs.](../index.md) |
| 401 - Authentication Fails | **Cause**: Authentication fails due to the wrong API key.   **Solution**: Please check your API key. If you don't have one, please [create an API key](https://platform.deepseek.com/api_keys) first. |
| 402 - Insufficient Balance | **Cause**: You have run out of balance.   **Solution**: Please check your account's balance, and go to the [Top up](https://platform.deepseek.com/top_up) page to add funds. |
| 408 - Request Timeout | **Cause**: The file upload was too slow, for example in the OCR or speech to text API.   **Solution**: Check your network and retry. See the limits in the guide of that API. |
| 413 - Request Too Large | **Cause**: The uploaded file is too large, for example in the OCR or speech to text API.   **Solution**: Reduce the file size. See the limits in the guide of that API. |
| 422 - Invalid Parameters | **Cause**: Your request contains invalid parameters.   **Solution**: Please modify your request parameters according to the hints in the error message. For more API format details, please refer to [DeepSeek API Docs.](../index.md) |
| 429 - Rate Limit Reached | **Cause**: You are sending requests too quickly, or have exceeded a concurrency or QPS limit.   **Solution**: Please pace your requests reasonably. For model rate limits, see [Rate Limit & Isolation](rate_limit.md). |
| 500 - Server Error | **Cause**: Our server encounters an issue.   **Solution**: Please retry your request after a brief wait and contact us if the issue persists. |
| 503 - Server Overloaded | **Cause**: The server is overloaded due to high traffic.   **Solution**: Please retry your request after a brief wait. |
| 504 - Gateway Timeout | **Cause**: The request did not finish within its time limit, for example in the OCR API or a document upload.   **Solution**: Retry later, or send a smaller file. |
