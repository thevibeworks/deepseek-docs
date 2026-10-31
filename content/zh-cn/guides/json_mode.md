---
title: "JSON Output"
description: "在很多场景下，用户需要让模型严格按照 JSON 格式来输出，以实现输出的结构化，便于后续逻辑进行解析。"
source: https://api-docs.deepseek.com/zh-cn/guides/json_mode
fetched: 2026-10-31
---

# JSON Output

在很多场景下，用户需要让模型严格按照 JSON 格式来输出，以实现输出的结构化，便于后续逻辑进行解析。

DeepSeek 提供了 JSON Output 功能，来确保模型输出合法的 JSON 字符串。

## 注意事项

1. 设置 `response_format` 参数为 `{'type': 'json_object'}`。
2. 用户传入的 system 或 user prompt 中必须含有 `json` 字样，并给出希望模型输出的 JSON 格式的样例，以指导模型来输出合法 JSON。
3. 需要合理设置 `max_tokens` 参数，防止 JSON 字符串被中途截断。
4. **在使用 JSON Output 功能时，如果模型的输出无法被识别为 JSON，API 会将其中的非 JSON 内容替换为空格（`U+0020`），因此返回的 `content` 可能仅包含空格（看起来为空，此时 `finish_reason` 仍可能是 `stop`）。您可以尝试修改 prompt 以缓解此类问题，并在代码中对空的 `content` 做兜底处理（例如重试请求）。**

## 样例代码

这里展示了使用 JSON Output 功能的完整 Python 代码：

```python
import json
from openai import OpenAI

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format.

EXAMPLE INPUT:
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    response_format={
        'type': 'json_object',
    },
)

print(json.loads(response.choices[0].message.content))
```

模型将会输出：

```text
{
    "question": "Which is the longest river in the world?",
    "answer": "The Nile River"
}
```
