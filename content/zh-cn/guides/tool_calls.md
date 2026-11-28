---
title: "Tool Calls"
description: "Tool Calls 让模型能够调用外部工具，来增强自身能力。"
source: https://api-docs.deepseek.com/zh-cn/guides/tool_calls/
fetched: 2026-11-28
---

# Tool Calls

Tool Calls 让模型能够调用外部工具，来增强自身能力。

---

## 非思考模式

### 样例代码

这里以获取用户当前位置的天气信息为例，展示了使用 Tool Calls 的完整 Python 代码。

Tool Calls 的具体 API 格式请参考[对话补全](../api/create-chat-completion.md)文档。

```python
from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        tools=tools,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return response.choices[0].message

client = OpenAI(
    api_key="<your api key>",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou, Zhejiang?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"Model>\t {message.content}")
```

这个例子的执行流程如下：

1. 用户：询问现在的天气
2. 模型：返回 function `get_weather({location: 'Hangzhou'})`
3. 用户：调用 function `get_weather({location: 'Hangzhou'})`，并传给模型。
4. 模型：返回自然语言，"The current temperature in Hangzhou is 24°C."

注：上述代码中 `get_weather` 函数功能需由用户提供，模型本身不执行具体函数。

---

## 思考模式

从 DeepSeek-V3.2 开始，API 支持了思考模式下的工具调用能力，详见[思考模式](thinking_mode.md#tool-calls)。

---

## 延迟加载工具

部分 Agent 客户端拥有很大的工具目录，但在一次对话中只想让模型看到少数几个工具。延迟加载工具（也叫动态加载工具或工具搜索）让客户端可以控制哪些工具定义进入模型上下文：可以先声明工具、等需要时再加载，也可以只在需要时才提供工具定义。这可以缩小上下文，也让模型更容易选择工具。

各 API 格式的支持情况如下：

| 能力 | Anthropic API | Responses API | Chat Completion API |
| --- | --- | --- | --- |
| 工具暂不放进 prompt，等加载后再使用 | 支持（`defer_loading`） | 支持（工具在 `tool_search_output` 中提供） | 不支持 |
| 在对话中途加载工具 | 支持 | 支持 | 不支持 |
| 模型支持 | `deepseek-flash` | `deepseek-flash` | — |

目前，`deepseek-v4-pro` 不支持延迟加载：Anthropic API 会忽略 `defer_loading`、`tool_addition` 和 `tool_reference` 的加载效果（`tool_reference` 会按工具名纯文本处理），所有已声明的工具从一开始就可用；Responses API 的 `tool_search` 工具声明以及 `tool_search_call` / `tool_search_output` item 也不会生效。

已加载的工具属于对话历史的一部分。API 是无状态的，因此后续每次请求都要回传完整对话历史（包括加载记录）；在 Anthropic API 中，还要把被延迟加载的工具以 `defer_loading: true` 继续声明在顶层 `tools` 数组中。工具加载后，在本次对话的剩余部分一直可用。

延迟加载也有利于上下文缓存：被延迟的工具定义不会进入开头的 system 提示词，加载工具时新的 schema 会追加在已有历史之后，而不是改动请求开头，因此之前已经落盘的缓存前缀仍然有效，只有新追加的部分是新增输入（缓存未命中）。相比之下，改变顶层 `tools` 数组中非延迟加载的工具集合会改变开头的提示词，可能导致之前的缓存前缀无法匹配。详见[上下文硬盘缓存](kv_cache.md)。

### Anthropic API

在顶层 `tools` 数组中，把需要延迟加载的工具标记为 `defer_loading: true`。这些工具会被声明，但初始不会展示给模型；请求中至少要有一个工具不带 `defer_loading`。

对于 `system_prompt_update` 为 `in-history` 的模型（见[模型列表 API](../api/list-models.md#responses)），对话中途的 `system` 消息会更新当前生效的 system 提示词；冲突时以更晚的为准（此前的 `system` 消息仍保留在历史中，不冲突的指令仍可能生效）。详见[对话中途的 system 消息](anthropic_api.md#mid-conversation-system-messages)。

当某个 `tool_reference` 块引用该工具时，工具会被加载。`tool_reference` 可以出现在以下两个位置：

- `user` 消息中 `tool_result` 块的 `content` 里；
- 对话中途 `system` 消息的 `tool_addition` 块的 `tool` 字段里。

使用 `tool_result` 时，客户端通常会提供一个普通工具（例如 `search_tools`）供模型调用并传入查询。被延迟的工具 schema 仍然不可见，因此模型需要其它途径知道可以加载哪些工具：可以在搜索工具的描述中说明工具目录，也可以插入一条 `system` 消息列出可加载的延迟工具。模型调用 `search_tools` 后，在下一次请求中把这条 assistant `tool_use` 块和对应的 `tool_result` 追加到历史里，并把命中的工具以 `tool_reference` 块的形式返回：

```json
{
  "model": "deepseek-flash",
  "max_tokens": 1024,
  "thinking": {"type": "disabled"},
  "tools": [
    {
      "name": "search_tools",
      "description": "Search the tool catalog for tools that can help with the user's request.",
      "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
      }
    },
    {
      "name": "get_weather",
      "description": "Get the current weather for a city.",
      "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
      },
      "defer_loading": true
    }
  ],
  "messages": [
    {"role": "user", "content": "杭州天气怎么样？"},
    {
      "role": "assistant",
      "content": [
        {"type": "tool_use", "id": "toolu_1", "name": "search_tools", "input": {"query": "weather"}}
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_1",
          "content": [{"type": "tool_reference", "tool_name": "get_weather"}]
        },
        {"type": "text", "text": "Continue."}
      ]
    }
  ]
}
```

`get_weather` 在历史的这个位置被加载，因此模型可以在同一次响应中调用它：

```json
{
  "stop_reason": "tool_use",
  "content": [
    {"type": "tool_use", "id": "toolu_2", "name": "get_weather", "input": {"city": "Hangzhou"}}
  ]
}
```

如果不想等待模型发起搜索调用，也可以在对话中途的 `system` 消息里直接放入 `tool_addition` 块来加载工具：

```json
{
  "role": "system",
  "content": [
    {"type": "tool_addition", "tool": {"type": "tool_reference", "name": "get_weather"}}
  ]
}
```

对话中途只支持增加工具：`tool_addition` 块或 `tool_reference` 块引用的工具都必须在顶层 `tools` 数组中声明。不支持 `tool_removal` 和内联 `tool_definition` 块。延迟加载不能与 `deepseek_web_search`、`deepseek_read_url` 同时使用。

### Responses API

Responses API 中，顶层 `tools` 数组里声明的 function 工具从一开始就可用，额外的工具通过 `tool_search` 在对话中途加载。发送一个在 `tools` 里包含客户端执行的 `tool_search` 工具的请求，它的 `description` 和 `parameters` 会告诉模型何时搜索、传什么参数。下面的例子关闭了思考模式，因此后续请求不需要回传思考 item：

```json
{
  "model": "deepseek-flash",
  "reasoning": {"effort": "none"},
  "tools": [
    {
      "type": "tool_search",
      "execution": "client",
      "description": "Search for tools that can help with the user's request.",
      "parameters": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
      }
    }
  ],
  "input": "杭州天气怎么样？"
}
```

当模型需要工具时，它会返回一个 `tool_search_call` 输出 item。下面的 `tsc_1` 和 `call_1` 分别是 item `id` 和 `call_id` 的占位值：

```json
{
  "type": "tool_search_call",
  "id": "tsc_1",
  "call_id": "call_1",
  "execution": "client",
  "status": "completed",
  "arguments": {"query": "weather"}
}
```

客户端在自己的工具目录中搜索，然后发送新的请求。新请求要重复原始输入和 `tool_search_call` item，并增加一个具有相同 `call_id` 的 `tool_search_output` item，在其自身的 `tools` 字段中放入命中工具的完整定义。回传 `tool_search_call` item 时，只需要 `type`、`call_id`、`execution` 和 `arguments`：

```json
{
  "model": "deepseek-flash",
  "reasoning": {"effort": "none"},
  "tools": [
    {
      "type": "tool_search",
      "execution": "client",
      "description": "Search for tools that can help with the user's request.",
      "parameters": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
      }
    }
  ],
  "input": [
    {"role": "user", "content": "杭州天气怎么样？"},
    {
      "type": "tool_search_call",
      "call_id": "call_1",
      "execution": "client",
      "arguments": {"query": "weather"}
    },
    {
      "type": "tool_search_output",
      "call_id": "call_1",
      "execution": "client",
      "tools": [
        {
          "type": "function",
          "name": "get_weather",
          "description": "Get the current weather for a city.",
          "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
          }
        }
      ]
    }
  ]
}
```

`tool_search_output.tools` 中的工具从输入的该位置起可用。模型可以像普通 function 工具一样调用它们；把每个结果作为 `function_call_output` item 返回并继续对话即可。仅支持 `execution: "client"`，服务端不执行工具搜索。`tool_search` 不能与 `deepseek_web_search`、`deepseek_read_url` 同时使用。

开启思考模式时，还要回传模型的 `reasoning` 输出 item，或者原样使用 API 返回的 `call_id`，以便服务端恢复思考内容。

### Chat Completion API

Chat Completion API 不支持延迟加载。`tools` 中的每个工具从请求开始时就对模型可用。要改变可用工具，只需在下一次请求中传入完整的新 `tools` 数组；对话历史不记录工具定义。

---

## 在对话中间插入工具调用

在部分 Agent 场景中，客户端需要把并非由模型生成的工具调用及其结果，插入到对话历史的中间。三种 API 格式都接受这样的历史，但要求的消息排列方式不同：

- **Anthropic API**：包含 `tool_use` 块的 assistant 消息后面必须紧跟一条 `user` 消息，且该消息开头的块是 `tool_result`，每个 `tool_use` ID 对应一个。
- **Responses API**：`function_call` 输入 item 后面必须紧跟具有相同 `call_id` 的 `function_call_output` item，且中间不能出现其它 message item；同一组调用的输出可以按任意顺序出现。
- **Chat Completion API**：带 `tool_calls` 的 assistant 消息后面必须紧跟每次调用对应的一条 `tool` 消息，且 `tool_call_id` 要匹配。API 会校验配对关系并拒绝重复 ID，但不会校验这些调用是否由模型生成，也不会校验工具是否已在 `tools` 中声明。

插入工具调用并不会声明或加载工具。在 Anthropic 和 Responses API 中，如果工具定义还不在对话里，请使用上文的延迟加载机制；在 Chat Completion API 中，只有当工具出现在顶层 `tools` 数组中时模型才能调用它，插入调用并不会把它加进去。

### 在对话中间插入 system 消息

三种 API 格式都支持在对话中间插入 `system` 消息：Anthropic 和 Chat Completion 格式使用 `role: "system"` 的消息，Responses API 使用 role 为 `system` 的 `message` item。`system` 消息不能把工具调用和它的结果拆开。

---

## `strict` 模式（Beta）

在 `strict` 模式下，模型在输出 Function 调用时会严格遵循 Function 的 JSON Schema 的格式要求，以确保模型输出的 Function 符合用户的定义。在思考与非思考模式下的工具调用，均可使用 `strict` 模式。

要使用 `strict` 模式，需要：

1. 用户需要设置 `base_url="https://api.deepseek.com/beta"` 来开启 Beta 功能
2. 在传入的 `tools` 列表中，所有 `function` 均需设置 `strict` 属性为 `true`
3. 服务端会对用户传入的 Function 的 JSON Schema 进行校验，如不符合规范，或遇到服务端不支持的 JSON Schema 类型，将返回错误信息

以下是 `strict` 模式下 tool 的定义样例：

```json
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "strict": true,
        "description": "Get weather of a location, the user should supply a location first.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"],
            "additionalProperties": false
        }
    }
}
```

---

### `strict` 模式支持的 JSON Schema 类型

- object
- string
- number
- integer
- boolean
- array
- enum
- anyOf

---

#### object 类型

object 定义一个包含键值对的深层结构，其中 properties 定义了对象中每个键（属性）的 schema。**每个 `object` 的所有属性均需设置为 `required`，且 `object` 中 `additionalProperties` 属性必须为 `false`**。

示例：

```json
{
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" }
    },
    "required": ["name", "age"],
    "additionalProperties": false
}
```

---

#### string 类型

- 支持的参数：
  - pattern：使用正则表达式来约束字符串的格式
  - format：使用预定义的常见格式进行校验，目前支持：
    - email：电子邮件地址
    - hostname：主机名
    - ipv4：IPv4 地址
    - ipv6：IPv6 地址
    - uuid：uuid
- 不支持的参数
  - minLength
  - maxLength

示例：

```json
{
    "type": "object",
    "properties": {
        "user_email": {
            "type": "string",
            "description": "The user's email address",
            "format": "email"
        },
        "zip_code": {
            "type": "string",
            "description": "Six digit postal code",
            "pattern": "^\\d{6}$"
        }
    }
}
```

---

#### number/integer 类型

- 支持的参数
  - const：固定数字为常数
  - default：数字的默认值
  - minimum：最小值
  - maximum：最大值
  - exclusiveMinimum：不小于
  - exclusiveMaximum：不大于
  - multipleOf：数字输出为这个值的倍数

示例：

```text
{
    "type": "object",
    "properties": {
        "score": {
            "type": "integer",
            "description": "A number from 1-5, which represents your rating, the higher, the better",
            "minimum": 1,
            "maximum": 5
        }
    },
    "required": ["score"],
    "additionalProperties": false
}
```

---

#### array 类型

- 不支持的参数
  - minItems
  - maxItems

示例：

```json
{
    "type": "object",
    "properties": {
        "keywords": {
            "type": "array",
            "description": "Five keywords of the article, sorted by importance",
            "items": {
                "type": "string",
                "description": "A concise and accurate keyword or phrase."
            }
        }
    },
    "required": ["keywords"],
    "additionalProperties": false
}
```

---

#### enum

enum 可以确保输出是预期的几个选项之一，例如在订单状态的场景下，只能是有限几个状态之一。

样例：

```text
{
    "type": "object",
    "properties": {
        "order_status": {
            "type": "string",
            "description": "Ordering status",
            "enum": ["pending", "processing", "shipped", "cancelled"]
        }
    }
}
```

---

#### anyOf

匹配所提供的多个 schema 中的任意一个，可以处理可能具有多种有效格式的字段，例如用户的账户可能是邮箱或者手机号中的一个：

```json
{
    "type": "object",
    "properties": {
    "account": {
        "anyOf": [
            { "type": "string", "format": "email", "description": "可以是电子邮件地址" },
            { "type": "string", "pattern": "^\\d{11}$", "description": "或11位手机号码" }
        ]
    }
  }
}
```

---

#### $ref 和 $def

可以使用 $def 定义模块，再用 $ref 引用以减少模式的重复和模块化，此外还可以单独使用 $ref 定义递归结构。

```json
{
    "type": "object",
    "properties": {
        "report_date": {
            "type": "string",
            "description": "The date when the report was published"
        },
        "authors": {
            "type": "array",
            "description": "The authors of the report",
            "items": {
                "$ref": "#/$def/author"
            }
        }
    },
    "required": ["report_date", "authors"],
    "additionalProperties": false,
    "$def": {
        "author": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "author's name"
                },
                "institution": {
                    "type": "string",
                    "description": "author's institution"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "author's email"
                }
            },
            "additionalProperties": false,
            "required": ["name", "institution", "email"]
        }
    }
}
```
