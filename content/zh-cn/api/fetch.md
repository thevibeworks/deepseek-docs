---
title: "网页抓取"
description: "抓取网页，返回页面标题与 Markdown 格式的内容。错误处理和计费说明请参考[网页搜索与抓取指南](/zh-cn/guides/search)。"
source: https://api-docs.deepseek.com/zh-cn/api/fetch
fetched: 2026-10-31
---

# 网页抓取

[打开 Markdown](https://api-docs.deepseek.com/zh-cn/api/fetch.md "在新标签页打开 Markdown")

```
POST /v1/tools/fetch
```

抓取网页，返回页面标题与 Markdown 格式的内容。错误处理和计费说明请参考[网页搜索与抓取指南](../guides/search.md)。

响应示例仅展示页面内容的摘录。

## Request

**[application/json]**

**Bodyrequired**

**url** stringrequired

**最少字符数：** `1`

**最多字符数：** `8192`

要抓取的网页地址，长度不超过 8192；必须为含 host 的 HTTP/HTTPS URL，且不能携带用户名或密码。

## Responses

- 200

OK, 返回抓取到的网页内容。

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**title** stringrequired

页面标题；缺失时为空字符串。

**content** stringrequired

抓取后的 Markdown 正文。

**[Example]**

```json
{
  "title": "首次调用 API | DeepSeek API Docs",
  "content": "# 首次调用 API\n\nDeepSeek API 使用与 OpenAI/Anthropic 兼容的 API 格式，通过修改配置，您可以使用 OpenAI/Anthropic SDK 来访问 DeepSeek API，或使用与 OpenAI/Anthropic API 兼容的软件。"
}
```

Loading...
