---
title: "图像理解"
description: "deepseek-v4-flash-vision-exp 模型支持在文本之外输入图片，你可以让模型描述图片、识别截图中的文字、分析图表等。"
source: https://api-docs.deepseek.com/zh-cn/guides/vision
fetched: 2026-08-23
---

# 图像理解

`deepseek-v4-flash-vision-exp` 模型支持在文本之外输入图片，你可以让模型描述图片、识别截图中的文字、分析图表等。

支持的图片格式：**JPEG、PNG、GIF、WebP**。格式由文件实际内容判断，而非文件名或声明的 MIME 类型。

---

## 传入图片

共有三种方式向模型提供图片，均使用标准的 OpenAI 兼容对话补全格式，即 `content` 为一个块（block）数组，而非纯字符串。同样的三种方式也适用于 [Responses API](responses_api.md#image-input)，图片以 `input_image` 内容块承载。

以下示例的 `base_url` 为 `https://api.deepseek.com`。

### 1. Base64 编码图片（内联）

将图片编码后以 `data:` URL 的形式直接嵌入请求。这是本地文件最简单的方式。编码后的数据会计入 **48 MiB** 请求体大小限制（见 [限制](#limits)）。

```python
import base64
from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

with open("image.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                },
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -d '{
    "model": "deepseek-v4-flash-vision-exp",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "这张图片里有什么？"},
          {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<BASE64_DATA>"}}
        ]
      }
    ]
  }'
```

### 2. 外部图片 URL

传入一个可公开访问的 `http(s)` 链接，模型会自动下载图片。URL 长度最多 **8192 个字符**，图片文件最大 **32 MiB**，且需在 **60 秒**内完成下载。如果链接超长，请改用 base64 data URL 或 Files API。

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "描述一下这张图片。"},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image.jpg"},
                },
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

### 3. 引用通过 Files API 上传的文件

通过 [Files API](files_api.md) 上传一次图片，之后在请求中用其 `file_id` 引用。当你需要在多个请求中复用同一张图片，或图片会让请求体超过 48 MiB 内联限制时，这是最佳选择。与内联图片不同，通过 Files API `file_id` 引用的图片最大可达 64 MiB，且不受 32 MiB 单图检查限制。

使用 `file` 内容块，填入返回的 `file_id`（形如 `file-api-...`）：

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

此外，`file` 块也可以通过 `file_data` 以 base64 形式内联携带图片（`file_data` 与 `file_id` 二者互斥）：

```json
{
  "type": "file",
  "file_data": "data:image/jpeg;base64,<BASE64_DATA>",
  "filename": "image.jpg"
}
```

---

## 细节级别（Detail Level）

对于 `image_url` 输入，你可以选填 `detail` 字段来控制图片的处理方式：

| 取值 | 行为 |
| --- | --- |
| `low` | 推理前将图片缩放到 512×512。当不需要精细视觉细节时更快、更省 token。 |
| `high` | 保留原图。（为兼容性提供，等价于 `original`。） |
| `original` | 保留原图。 |
| `auto` | 自动选择。当前等价于 `original`。 |

```json
{
  "type": "image_url",
  "image_url": {"url": "https://example.com/image.jpg", "detail": "low"}
}
```

---

## 何时使用 Files API

内联图片（base64 或 `file_data`）会计入 **48 MiB** 的请求体大小限制。以下情况建议使用 [Files API](files_api.md)：

- 单个请求会超过请求体大小限制。
- 图片超过 32 MiB（只有通过 Files API 才能使用）。
- 你在多个请求中引用同一张图片，希望避免每次重复上传。

---

## Token 用量

图片会根据其尺寸换算成 token，并与文本 token 一起计费。

在进入模型前，每张图片都会被自动缩放：

- 总像素小于约 384×384 的图片会被保持长宽比放大；
- 更大的图片会被保持长宽比缩小，缩小后的总像素约相当于 **800×800** 的图片。

因此，每张图片消耗的 token 数存在上限（**384** 个）：例如 2000×2000 和 5000×5000 的图片，经缩放后消耗的 token 数是相同的。单个请求包含多张图片时，每张图片独立按同一规则计算，不存在额外的计算方式。

如需估算具体尺寸图片的 token 消耗，请使用 [Token 与用量计算](../quick_start/token_usage.md) 页面的图片 Token 计算器。

---

## 限制

| 限制项 | 数值 |
| --- | --- |
| 支持的格式 | JPEG、PNG、GIF、WebP |
| 外部 URL 长度 | 8192 个字符 |
| 请求体大小 | 48 MiB |
| 单张图片最大大小（base64 / 外部 URL） | 32 MiB |
| 单张图片最大大小（Files API `file_id`） | 64 MiB |
| 单个请求最大图片数 | 600 |
| 单个请求图片总大小 | 不含 `file_id` 图片最多 64 MiB；包含 `file_id` 图片最高 200 MiB |
| 图片最大尺寸 | 单边最长 8192 像素；单个请求包含 15 张及以上图片时，降为单边最长 4096 像素 |

Files API 上传文件的存储与上传配额见 [Files API：限制](files_api.md#limits)。

---

## 使用限制

- 图片仅支持出现在 `user` 消息中：`system` 或 `assistant` 消息携带图片会返回 `400` 错误。
- 仅视觉模型（`deepseek-v4-flash-vision-exp`）接受图片，其他模型会返回 `400` 错误（“This model does not support image”）。
- 用户文本包含保留的图片占位 token 会被拒绝并返回 `400` 错误。

---

## 在 Anthropic API 中使用图片

除了上面的 OpenAI 兼容端点，你也可以通过 Anthropic 兼容的 `/messages` 端点发送图片（`base_url` 为 `https://api.deepseek.com/anthropic`）。基础配置请参考 [Anthropic API](anthropic_api.md)。

区别在于图片内容块的结构。Anthropic 不使用 `image_url`，而是使用 `image` 块，其 `source` 对象的 `type` 为 `base64`、`url` 或 `file` 之一：

```python
import anthropic

client = anthropic.Anthropic()  # ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic

message = client.messages.create(
    model="deepseek-v4-flash-vision-exp",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "<BASE64_DATA>",
                    },
                },
            ],
        }
    ],
)
print(message.content)
```

三种 `source` 变体与上面的 OpenAI 方式一一对应：

| `source.type` | 对应的 OpenAI 方式 | 说明 |
| --- | --- | --- |
| `base64` | Base64 编码图片 | 需要 `media_type` 字段（`image/jpeg`、`image/png`、`image/gif` 或 `image/webp`）。 |
| `url` | 外部图片 URL | 最多 8192 个字符。 |
| `file` | Files API `file_id` | 需要请求头 `anthropic-beta: files-api-2025-04-14`。 |

---

## 在 Responses API 中使用图片

`deepseek-v4-flash-vision-exp` 模型同样支持通过 OpenAI 兼容的 [Responses API](responses_api.md#image-input) 传入图片。三种传入方式（base64 data URL、外部 `http(s)` URL、Files API `file_id`）与[限制](#limits)均与上文一致，只有内容块的结构不同——图片以 `input_image` 内容块承载，可出现在 `user` / `developer` 消息或 `function_call_output` / `custom_tool_call_output` item 的 `output` 中：

```python
response = client.responses.create(
    model="deepseek-v4-flash-vision-exp",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "这张图片里有什么？"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg", "detail": "low"},
            ],
        }
    ],
)
print(response.output_text)
```

`input_image` 内容块支持 `detail` 字段，语义与上文一致（`low` / `high` / `original` / `auto`）。通过 `file_id` 传图时 `detail` 被忽略；`image_url` 与 `file_id` 互斥。

字段语义、使用限制（`system` / `assistant` 消息中的图片会返回 `400` 错误）以及工具输出中的图片，请参阅 [Responses API 指南](responses_api.md#image-input)。
