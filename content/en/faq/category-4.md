---
title: "FAQ: API"
description: "DeepSeek FAQ, API — 15 questions and answers."
source: https://static.deepseek.com/faq/index.html?lang=en#/category/4
fetched: 2026-08-05
---

# FAQ: API

## How to Top Up?

You can top up online via PayPal, bank card, Alipay, or WeChat Pay on the [「Top Up」](https://platform.deepseek.com/top_up) page. You can check the results on the [「Billing」](https://platform.deepseek.com/transactions) page.

## Incorrect Top-up Balance

If your previous top-up balance appears to be missing, it usually means you topped up with a different account than the one you're currently logged into. Here's how to find the correct account:

- If you have a Google or email login, try signing in with that method and check whether your top-up records are there.
- Go to the order details page of your Alipay or WeChat top-up transaction — the account used is listed under the **Product** field.
- If you deactivated and re-registered your account, your old and new accounts are separate, and the previous balance cannot be transferred. To request a refund, please [submit a ticket,](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg) select 「Refund Request」, and provide the necessary information.

## Does the balance expire?

Top-up balances do not expire.

## Is a refund possible?

Unused balances can be refunded.

- **Online Payment:** Log in to the Platform, go to [「Billing」](https://platform.deepseek.com/transactions), and click 「Refunds」 to complete the refund.
- **Corporate Bank Transfer:** You must [submit a ticket](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg). Select 「Refund Request」 and provide the necessary information.

## How to request an invoice

Log in to the Platform, go to [「Billing」](https://platform.deepseek.com/transactions), and click 「Invoices」 to apply.

You can also cancel and reissue invoices from the same page.

## Can usage details be added to the invoice?

Log in to the Platform, go to [「Billing」](https://platform.deepseek.com/transactions), click 「Invoices」, and enter the relevant information in the 「Remarks」 field.

## How to view usage by API Keys

To view detailed usage for each API key:

- Log in to the Platform and go to the [「Usage」](https://platform.deepseek.com/usage) page.
- Select your desired time range from the 「Time」 menu and the key you wish to query from the 「API Key」 menu.
- You can also click 「Export」 to download the usage zip file. Unzip it to find two csv files; the file titled **amount** contains usage details by Key.

## What to do if your API Key is leaked

To best protect your account and assets, we strongly recommend revoking the compromised key immediately. Here's how:

- Log in to the Platform and go to the [「API Keys」](https://platform.deepseek.com/api_keys) page.
- Locate the key you wish to revoke in the list, then click the 「trash bin」 icon.
- In the confirmation dialog, click 「Revoke」 to confirm.
- The "API Key revoked" message confirms the key has been immediately revoked and can no longer be viewed or modified.
- After revocation, please create a new API key and replace it in your application as soon as possible to avoid any disruption to your service.

As a reminder, please keep your API keys safe — never share them with others or expose them in browsers or client-side code.

## Do you support signing cooperation agreements?

DeepSeek API is provided via a self-service and standardized model. If you have specific offline agreement needs (such as *app filing* or *enterprise vendor onboarding*), please fill out a [「Cooperation Agreement Application」](https://trtgsjkv6r.feishu.cn/share/base/form/shrcn99HCMzQYKjO2r44fd3ACob)ticket and submit the relevant information. We will assist you with the request.

Note: The agreement is a standard framework agreement and cannot be modified. To view it, please log in to the [「Bank Transfer」](https://platform.deepseek.com/top_up)page to download the template.

## Are there plans with higher rate limits?

There is a unified pricing standard and no tiered plans. Please refer to the [API Pricing page](https://api-docs.deepseek.com/quick_start/pricing/) for details.

If you need higher rate limits, you can submit a [Rate Limit Increase Request](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnda9jNKvhyYr8xb843xLEzc). We'll match it to an appropriate level based on your actual needs — at no additional cost.

## Real-Name Verification Failed

Common reasons for verification failure are as follows:

- The number of accounts bound to this ID number exceeds the limit. Please delete some of the bound accounts and try again.
- The ID number has been entered incorrectly too many times consecutively, and the verification function will be temporarily locked.

If you need further assistance, please [submit a ticket](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg), select 「Account Login/Registration」to provide the relevant information.

## What is the difference between Personal and Enterprise Real-Name Verification?

There is currently no difference in user benefits or product features between Personal and Enterprise Verified accounts, although the verification methods and required materials differ. Please complete verification based on your actual account usage to ensure compliance.

## Can a Personal Account be changed to an Enterprise Verified Account?

Yes, you can update your verification via the following path:

[Top-up](https://platform.deepseek.com/top_up) → Bank Transfer → Enterprise Verification → Proceed to change

The change will not affect your account balance or current usage.

## Can an Enterprise Verified Account be changed to a Personal Account?

An Enterprise Verified Account cannot be changed to a Personal Account or transferred to a different enterprise.

## Why does the API keep returning empty lines?

After your request is sent, it may sometimes take a while to receive a response from the server. During this period, your HTTP request will remain connected, and you may continuously receive contents in the following formats:

- Non-streaming requests: Continuously return empty lines
- Streaming requests: Continuously return SSE keep-alive comments (`: keep-alive`)

These contents do not affect the parsing of the JSON body of the response. If you are parsing the HTTP responses yourself, please ensure to handle these empty lines or comments appropriately.

If the request has not started inference after 10 minutes, the server will close the connection.
