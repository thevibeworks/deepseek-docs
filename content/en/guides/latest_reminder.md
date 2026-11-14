---
title: "User Metadata Marker"
description: "DeepSeek Chat tells the model the current date and the user's location, platform and language, so that answers fit the user's situation. With the API, you provide this information in a latest_reminder message."
source: https://api-docs.deepseek.com/guides/latest_reminder
fetched: 2026-11-14
---

# User Metadata Marker

DeepSeek Chat tells the model the current date and the user's location, platform and language, so that answers fit the user's situation. With the API, you provide this information in a `latest_reminder` message.

Format: `<date>,<weekday>,<location>,<platform>,<language>`

| Field | Description |
| --- | --- |
| `date` | `YYYY-MM-DD` |
| `weekday` | The weekday of `date`, written in the language given by `language`, for example `Monday` or `星期一` |
| `location` | Optional, can be empty, and may contain commas |
| `platform` | `App` or `Web` |
| `language` | The language name written in that language, for example `English` or `中文` |

Example: `2026-11-09,Monday,Singapore,Web,English`

Put a message `{"role": "latest_reminder", "content": "..."}` in `messages`, directly before the `user` message it belongs to. It works in the Messages API, with or without the web tools, and in the Chat Completions API. The Responses API does not accept it.

**[Messages]**

```bash
curl https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {"role": "latest_reminder", "content": "2026-11-10,Tuesday,Singapore,Web,English"},
      {"role": "user", "content": "What is DeepSeek?"},
      {"role": "assistant", "content": "DeepSeek is ..."},
      {"role": "latest_reminder", "content": "2026-11-11,Wednesday,Singapore,Web,English"},
      {"role": "user", "content": "What is in the news today?"}
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
      {"role": "latest_reminder", "content": "2026-11-10,Tuesday,Singapore,Web,English"},
      {"role": "user", "content": "What is DeepSeek?"},
      {"role": "assistant", "content": "DeepSeek is ..."},
      {"role": "latest_reminder", "content": "2026-11-11,Wednesday,Singapore,Web,English"},
      {"role": "user", "content": "What is in the news today?"}
    ]
  }'
```

- As in DeepSeek Chat, each round can have its own message of this kind. Pass those of earlier rounds back with the history; leaving them out is allowed, but lowers context cache hits.
- `content` must be a string; otherwise the request body cannot be parsed and returns `422`. A value that does not match the format returns `400` and names the invalid field.
- The message must be directly followed by a `user` message; otherwise the request returns `400`. It cannot be placed between a `tool_use` and its `tool_result`.
- Links in this message are not read, and the message does not affect whether the model searches.
- The `latest_reminder` role is not in the message types of the Anthropic SDKs, but the SDKs do not check it at runtime. In Python, pass the dictionary as it is, with `# type: ignore` for type checkers.

**Supported language values**

`Afrikaans`, `አማርኛ`, `العربية`, `Azərbaycanca`, `беларуская`, `български`, `বাংলা`, `català`, `čeština`, `dansk`, `Deutsch`, `Ελληνικά`, `English`, `español`, `eesti`, `euskara`, `فارسی`, `suomi`, `Filipino`, `français`, `galego`, `ગુજરાતી`, `עברית`, `हिन्दी`, `hrvatski`, `magyar`, `հայերեն`, `Indonesia`, `íslenska`, `italiano`, `日本語`, `ქართული`, `қазақтілі`, `ខ្មែរ`, `ಕನ್ನಡ`, `한국어`, `кыргызча`, `ລາວ`, `lietuvių`, `latviešu`, `македонски`, `മലയാളം`, `монгол`, `मराठी`, `Melayu`, `မြန်မာ`, `नेपाली`, `Nederlands`, `ਪੰਜਾਬੀ`, `polski`, `português`, `română`, `русский`, `සිංහල`, `slovenčina`, `slovenščina`, `shqip`, `српски`, `svenska`, `Kiswahili`, `தமிழ்`, `తెలుగు`, `ไทย`, `Türkçe`, `українська`, `اردو`, `TiếngViệt`, `中文`, `中文繁體`, `中文香港`, `isiZulu`
