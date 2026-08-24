---
title: "Vision"
description: "The deepseek-v4-flash-vision-exp model accepts images alongside text, so you can ask the model to describe pictures, read text from screenshots, analyze charts, and more."
source: https://api-docs.deepseek.com/guides/vision
fetched: 2026-08-23
---

# Vision

The `deepseek-v4-flash-vision-exp` model accepts images alongside text, so you can ask the model to describe pictures, read text from screenshots, analyze charts, and more.

Supported image formats: **JPEG, PNG, GIF, and WebP**. The format is detected from the actual file content, not from the file name or the declared MIME type.

---

## Sending Images

There are three ways to provide an image to the model. All of them use the standard OpenAI-compatible Chat Completions format, where `content` is an array of blocks instead of a plain string. The same three methods are also available in the [Responses API](responses_api.md#image-input), where images are carried in `input_image` content parts.

The `base_url` for the examples below is `https://api.deepseek.com`.

### 1. Base64-encoded image (inline)

Encode the image and embed it directly in the request as a `data:` URL. This is the simplest option for local files. The encoded data counts toward the **48 MiB** request body limit (see [Limits](#limits)).

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
                {"type": "text", "text": "What is in this image?"},
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
          {"type": "text", "text": "What is in this image?"},
          {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<BASE64_DATA>"}}
        ]
      }
    ]
  }'
```

### 2. External image URL

Pass a publicly accessible `http(s)` link and the model downloads the image for you. The URL must be at most **8192 characters**, the image file may be at most **32 MiB**, and the download must complete within **60 seconds**. If your link is longer, use a base64 data URL or the Files API instead.

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image."},
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

### 3. Reference a file uploaded via the Files API

Upload an image once with the [Files API](files_api.md), then reference its `file_id` in your requests. This is the best option when you reuse the same image across multiple requests, or when the image pushes the request body over the 48 MiB inline limit. Unlike inline images, images referenced via Files API `file_id` may be up to 64 MiB and are not subject to the 32 MiB per-image check.

Use a `file` content block with the returned `file_id` (which has the form `file-api-...`):

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash-vision-exp",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "file", "file_id": "file-api-xxxxxxxxxxxxxxxx"},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

Alternatively, a `file` block can carry the image inline as base64 via `file_data` instead of `file_id` (the two are mutually exclusive):

```json
{
  "type": "file",
  "file_data": "data:image/jpeg;base64,<BASE64_DATA>",
  "filename": "image.jpg"
}
```

---

## Detail Level

For `image_url` inputs you can optionally set a `detail` field to control how the image is processed:

| Value | Behavior |
| --- | --- |
| `low` | The image is downscaled to 512×512 before inference. Faster and cheaper when fine visual detail is not important. |
| `high` | Keeps the original image. (Provided for compatibility; equivalent to `original`.) |
| `original` | Keeps the original image. |
| `auto` | Automatic selection. Currently equivalent to `original`. |

```json
{
  "type": "image_url",
  "image_url": {"url": "https://example.com/image.jpg", "detail": "low"}
}
```

---

## When to Use the Files API

Inline images (base64 or `file_data`) count toward the request body size limit of **48 MiB**. Consider the [Files API](files_api.md) when:

- A single request would exceed the body size limit.
- The image is larger than 32 MiB, which is only possible through the Files API.
- You reference the same image in multiple requests and want to avoid re-uploading it each time.

---

## Token Usage

Images are converted into tokens based on their dimensions, and these tokens are billed together with your text tokens.

Before inference, every image is automatically resized:

- Images with a total pixel count below roughly 384×384 are scaled up while preserving their aspect ratio.
- Larger images are scaled down while preserving their aspect ratio, so that the total pixel count after resizing is roughly that of an **800×800** image.

As a result, there is an upper bound of **384** tokens per image: for example, a 2000×2000 image and a 5000×5000 image consume the same number of tokens after resizing. When a request contains multiple images, each image is counted independently under the same rule — there is no separate calculation for multi-image requests.

To estimate the token cost of an image of a specific size, use the image token calculator on the [Token & Token Usage](../quick_start/token_usage.md) page.

---

## Limits

| Limit | Value |
| --- | --- |
| Supported formats | JPEG, PNG, GIF, WebP |
| External URL length | 8192 characters |
| Request body size | 48 MiB |
| Max single image size (base64 / external URL) | 32 MiB |
| Max single image size (Files API `file_id`) | 64 MiB |
| Max images per request | 600 |
| Max total image size per request | 64 MiB without `file_id` images; up to 200 MiB including `file_id` images |
| Max image dimension | 8192 px per side; drops to 4096 px per side when a request contains 15 or more images |

For storage and upload quotas of files uploaded via the Files API, see [Files API: Limits](files_api.md#limits).

---

## Restrictions

- Images are supported in `user` messages only: images in `system` or `assistant` messages return a `400` error.
- Only vision models (`deepseek-v4-flash-vision-exp`) accept images; other models return a `400` error ("This model does not support image").
- User text containing the reserved image placeholder token is rejected with a `400` error.

---

## Using Images with the Anthropic API

In addition to the OpenAI-compatible endpoint above, you can send images through the Anthropic-compatible `/messages` endpoint (`base_url` = `https://api.deepseek.com/anthropic`). For general setup, see [Anthropic API](anthropic_api.md).

The difference is the shape of the image content block. Instead of `image_url`, Anthropic uses an `image` block with a `source` object whose `type` is one of `base64`, `url`, or `file`:

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
                {"type": "text", "text": "What is in this image?"},
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

The three `source` variants mirror the OpenAI methods above:

| `source.type` | Equivalent OpenAI method | Notes |
| --- | --- | --- |
| `base64` | Base64-encoded image | Requires a `media_type` field (`image/jpeg`, `image/png`, `image/gif`, or `image/webp`). |
| `url` | External image URL | Max 8192 characters. |
| `file` | Files API `file_id` | Requires the header `anthropic-beta: files-api-2025-04-14`. |

---

## Using Images with the Responses API

The `deepseek-v4-flash-vision-exp` model also accepts images through the OpenAI-compatible [Responses API](responses_api.md#image-input). The same three input methods (base64 data URL, external `http(s)` URL, Files API `file_id`) and the same [limits](#limits) apply; only the content part shape differs — images are carried in `input_image` parts, either in `user` / `developer` messages or in the output of `function_call_output` / `custom_tool_call_output` items:

```python
response = client.responses.create(
    model="deepseek-v4-flash-vision-exp",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image?"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg", "detail": "low"},
            ],
        }
    ],
)
print(response.output_text)
```

The `input_image` part supports a `detail` field with the same semantics as above (`low` / `high` / `original` / `auto`). `detail` is ignored when the image is provided via `file_id`, and `image_url` and `file_id` are mutually exclusive.

For field semantics, restrictions (images in `system` / `assistant` messages are rejected with a `400` error), and tool-output images, see the [Responses API guide](responses_api.md#image-input).
