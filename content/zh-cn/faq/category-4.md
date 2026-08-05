---
title: "FAQ: API相关"
description: "DeepSeek FAQ, API相关 — 15 questions and answers."
source: https://static.deepseek.com/faq/index.html?lang=zh#/category/4
fetched: 2026-08-05
---

# FAQ: API相关

## 如何充值

- 在线充值：完成实名认证后，您可以在[「充值」](https://platform.deepseek.com/top_up)页面使用支付宝/微信进行在线充值。您可以在[「账单」](https://platform.deepseek.com/transactions)页面查询充值结果。
- 对公汇款：对公汇款仅支持企业用户（暂时仅对 +86 手机号注册用户开放）。完成企业实名认证后，可获取专属汇款账号，向专属汇款账号进行打款。为保证汇款顺利进行，**请确保汇款方开户名称与开放平台实名认证名称一致**。我方银行账户到账后，汇款金额将在 10 分钟- 1 小时左右自动转入您的开放平台账户，如未及时收到，请联系我们。

## 充值余额金额不对

发现历史充值余额不存在时，通常是您充值的账号与当前登录的账号不同所致，可根据以下方式找回正确的登录账号：

- 如果您有 Google/邮箱登录账号，可尝试用 Google/邮箱 登录，检查充值记录是否存在于该账号下。
- 您可前往支付宝/微信充值订单详情页，在“商品”条目下，查询对应的充值账号。
- 如果您注销过账号后，重新注册，则新旧账号相互独立，原账号余额无法在新账号使用。如需处理，请填写[工单](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg)，选择「申请退款」选项，按照指引提交相关信息。

## 余额是否会过期

您的充值余额永久有效，不会过期。

## 是否可以退款

未消费金额支持退款。

- 在线支付：您可登录开放平台，在[「账单」](https://platform.deepseek.com/transactions)页面点击「退款管理」自助操作退款。
- 企业对公转账：需填写[工单](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg)，选择「申请退款」选项，按照指引提交相关信息。

## 如何申请发票

登录开放平台后，进入[「账单」](https://platform.deepseek.com/transactions)页面，点击「发票管理」即可提交开票申请。

您同样可以在「发票管理」界面申请发票作废，并重新开具。

## 开票是否能增加使用明细

登录开放平台后，进入[「账单」](https://platform.deepseek.com/transactions)页面，点击「发票管理」，在「备注信息」栏，填入相关信息。

## 如何分 key 查看用量

查看各 API Key 的详细用量步骤如下：

登录开放平台，进入「[用量信息](https://platform.deepseek.com/usage)」页面。

- 在「时间维度」菜单中选择需查询的时间范围，在「API Key」菜单中选中需查询的 key。
- 您也可以点击「导出」按钮，下载并解压用量信息压缩包，您将看到两个 CSV 文件。其中标题为 *amount* 的文件，即包含了分 Key 统计的用量明细。

## 若发现 API key 泄漏怎么办

为了最大程度保护您的账户和资产安全，我们建议您立即删除泄漏的 Key。具体操作步骤如下：

- 登录开放平台，进入[「API keys」](https://platform.deepseek.com/api_keys)页面。
- 在 Key 列表中，找到并选中需删除的 Key，点击「回收箱」图标。
- 在弹出的确认框中，点击「删除」按钮完成二次确认。
- 看到“API Key 已删除”的提示，即表示该 Key 已成功删除并立即失效，您将无法再查看或修改此 API key。
- 删除后，建议尽快创建新的 API Key 并替换到您的应用中，以免影响业务正常使用。

此外请注意妥善保存您的 API key，不要与他人共享，或将其暴露在浏览器或其他客户端代码中。

## 是否支持签订合作协议

DeepSeek API 主要通过自助及标准化的方式提供服务，若确有线下合作协议签订需求，如应用程序备案或企业入库，您可填写[合作协议申请工单](https://trtgsjkv6r.feishu.cn/share/base/form/shrcn99HCMzQYKjO2r44fd3ACob)，提交相关信息，我们将协助您处理。

注：所提供的协议为标准化框架协议，暂不支持条款修改，如需查看请登录[「对公汇款」](https://platform.deepseek.com/top_up)页面下载参考模版。

## 是否有限速更高的套餐

目前我们实行统一的 API 收费标准，暂无分级套餐。具体价格详情请查阅 [API 价格页面](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)。

若您有更高的并发需求，可提交[账号扩容申请工单](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnda9jNKvhyYr8xb843xLEzc)，我们将根据您实际的业务需求匹配合适的并发量，扩容并不增加额外的费用。

## 实名认证失败

认证失败常见原因如下：

- 该证件号绑定的账号超出数量限制，请注销部分已绑定账号后重试。
- 证件号连续输错次数较多，认证功能会被暂时锁定。

如需进一步协助，可填写[工单](https://trtgsjkv6r.feishu.cn/share/base/form/shrcnhcHE4A6lQaQ3v0raCXmBAg)，问题反馈选择「账号登录/注册」选项，按照指引提交相关信息。

## 个人实名认证与企业实名认证有什么区别？

个人认证账号与企业认证账号在用户权益和产品功能上目前无差异。主要区别在于认证所需材料和流程不同。请您根据账号的实际使用主体，选择合规的认证类型。

## 个人认证账号可以更改为企业实名账号吗？

可以，您可以通过以下路径变更认证：

[「充值」](https://platform.deepseek.com/top_up)页面 →「对公汇款」→「企业实名认证」→「去变更」。

变更不会影响账户余额和当前正常使用。

## 企业实名账号可以更改为个人账号吗？

已完成企业实名认证的账号，其认证类型不可变更为个人认证或其他企业认证。

## 为什么调用 API 时，持续返回空行？

您的请求发出后，有时需要等待一段时间才能获取服务器的响应。在这段时间里，您的 HTTP 请求会保持连接，并持续收到如下格式的返回内容：

- 非流式请求：持续返回空行
- 流式请求：持续返回 SSE keep-alive 注释（`: keep-alive`）

这些内容不影响对响应的 JSON body 的解析。如果您在自己解析 HTTP 响应，请注意处理这些空行或注释。

如果 10 分钟后，请求仍未开始推理，服务器将关闭连接。
