---
title: "用户元信息标记"
description: "DeepSeek 网页端会把当前日期、用户所在地、平台和语言告诉模型，让回答更贴合用户的情况。使用 API 时，这些信息由你通过一条 latest_reminder 消息提供。"
source: https://api-docs.deepseek.com/zh-cn/guides/latest_reminder
fetched: 2026-11-14
---

# 用户元信息标记

DeepSeek 网页端会把当前日期、用户所在地、平台和语言告诉模型，让回答更贴合用户的情况。使用 API 时，这些信息由你通过一条 `latest_reminder` 消息提供。

格式：`<date>,<weekday>,<location>,<platform>,<language>`

| 字段 | 说明 |
| --- | --- |
| `date` | `YYYY-MM-DD` |
| `weekday` | `date` 当天是星期几，用 `language` 对应的语言书写，例如 `Monday` 或 `星期一` |
| `location` | 可选，可以为空，可以包含逗号 |
| `platform` | `App` 或 `Web` |
| `language` | 用该语言自身书写的语言名，例如 `English` 或 `中文` |

示例：`2026-11-09,星期一,新加坡,Web,中文`

在 `messages` 中传入 `{"role": "latest_reminder", "content": "..."}`，紧挨在它所属的 `user` 消息之前。Messages API（无论是否使用联网工具）与 Chat Completions API 都支持。Responses API 不支持。

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "latest_reminder", "content": "2026-11-10,星期二,新加坡,Web,中文"},
      {"role": "user", "content": "DeepSeek 是什么？"},
      {"role": "assistant", "content": "DeepSeek 是……"},
      {"role": "latest_reminder", "content": "2026-11-11,星期三,新加坡,Web,中文"},
      {"role": "user", "content": "今天有什么新闻"}
    ]
  }'
```

**[Chat Completions]**

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "latest_reminder", "content": "2026-11-10,星期二,新加坡,Web,中文"},
      {"role": "user", "content": "DeepSeek 是什么？"},
      {"role": "assistant", "content": "DeepSeek 是……"},
      {"role": "latest_reminder", "content": "2026-11-11,星期三,新加坡,Web,中文"},
      {"role": "user", "content": "今天有什么新闻"}
    ]
  }'
```

- 与 DeepSeek 网页端一样，每一轮都可以带一条这样的消息。请随历史一起回传之前各轮的这类消息；不回传也可以，但会降低上下文缓存命中。
- `content` 必须是字符串，否则请求体无法解析，返回 `422`。格式不符时返回 `400`，并指出不合法的字段。
- 这条消息后面必须紧跟一条 `user` 消息，否则返回 `400`。也不能放在 `tool_use` 与对应的 `tool_result` 之间。
- 这条消息里的链接不会被阅读，也不影响是否搜索。
- `latest_reminder` 角色不在 Anthropic SDK 的消息类型中，但 SDK 运行时不校验。Python 直接传字典即可，类型检查器需要加 `# type: ignore`。

**支持的语言取值**

`Afrikaans`, `አማርኛ`, `العربية`, `Azərbaycanca`, `беларуская`, `български`, `বাংলা`, `català`, `čeština`, `dansk`, `Deutsch`, `Ελληνικά`, `English`, `español`, `eesti`, `euskara`, `فارسی`, `suomi`, `Filipino`, `français`, `galego`, `ગુજરાતી`, `עברית`, `हिन्दी`, `hrvatski`, `magyar`, `հայերեն`, `Indonesia`, `íslenska`, `italiano`, `日本語`, `ქართული`, `қазақтілі`, `ខ្មែរ`, `ಕನ್ನಡ`, `한국어`, `кыргызча`, `ລາວ`, `lietuvių`, `latviešu`, `македонски`, `മലയാളം`, `монгол`, `मराठी`, `Melayu`, `မြန်မာ`, `नेपाली`, `Nederlands`, `ਪੰਜਾਬੀ`, `polski`, `português`, `română`, `русский`, `සිංහල`, `slovenčina`, `slovenščina`, `shqip`, `српски`, `svenska`, `Kiswahili`, `தமிழ்`, `తెలుగు`, `ไทย`, `Türkçe`, `українська`, `اردو`, `TiếngViệt`, `中文`, `中文繁體`, `中文香港`, `isiZulu`
