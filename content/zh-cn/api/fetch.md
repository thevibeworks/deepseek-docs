---
title: "网页抓取"
description: "抓取网页，返回页面标题与 Markdown 格式的内容。错误处理和计费说明请参考[网页搜索与抓取指南](/zh-cn/guides/search)。"
source: https://api-docs.deepseek.com/zh-cn/api/fetch
fetched: 2026-10-17
---

# 网页抓取

```
POST /v1/tools/fetch
```

抓取网页，返回页面标题与 Markdown 格式的内容。错误处理和计费说明请参考[网页搜索与抓取指南](../guides/search.md)。

## Request

**[application/json]**

**Bodyrequired**

**url** stringrequired

**Possible values:** `non-empty` and `<= 8192 characters`

要抓取的网页地址，长度不超过 8192；必须为含 host 的 HTTP/HTTPS URL，且不能携带用户名或密码。

## Responses

- 200

OK, 返回抓取到的网页内容。

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**title** stringrequired

页面标题；缺失时为空字符串。

**content** stringrequired

抓取后的 Markdown 正文。

**[Example (from schema)]**

```json
{
  "title": "string",
  "content": "string"
}
```

**[Example]**

```json
{
  "title": "Example article",
  "content": "# Example article\n\nArticle content."
}
```

Loading...
