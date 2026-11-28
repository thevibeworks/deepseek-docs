---
title: "Tool Calls"
description: "Tool Calls allows the model to call external tools to enhance its capabilities."
source: https://api-docs.deepseek.com/guides/tool_calls/
fetched: 2026-11-28
---

# Tool Calls

Tool Calls allows the model to call external tools to enhance its capabilities.

---

## Non-thinking Mode

### Sample Code

Here is an example of using Tool Calls to get the current weather information of the user's location, demonstrated with complete Python code.

For the specific API format of Tool Calls, please refer to the [Chat Completion](../api/create-chat-completion.md) documentation.

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

The execution flow of this example is as follows:

1. User: Asks about the current weather in Hangzhou
2. Model: Returns the function `get_weather({location: 'Hangzhou'})`
3. User: Calls the function `get_weather({location: 'Hangzhou'})` and provides the result to the model
4. Model: Returns in natural language, "The current temperature in Hangzhou is 24°C."

Note: In the above code, the functionality of the `get_weather` function needs to be provided by the user. The model itself does not execute specific functions.

---

## Thinking Mode

From DeepSeek-V3.2, the API supports tool use in the thinking mode. For more details, please refer to [Thinking Mode](thinking_mode.md#tool-calls).

---

## Deferred Tool Loading

Some agent clients have a large tool catalog but only want to expose a few tools to the model in a given conversation. With deferred tool loading (also called dynamic tool loading or tool search), the client controls which tool definitions enter the model's context: tools can be declared up front and loaded later, or supplied only when they are needed. This keeps the context small and makes tool selection easier. Support differs across API formats:

| Capability | Anthropic API | Responses API | Chat Completion API |
| --- | --- | --- | --- |
| Keep a tool out of the prompt until it is loaded | Supported (`defer_loading`) | Supported (tool supplied in `tool_search_output`) | Not supported |
| Load a tool in the middle of a conversation | Supported | Supported | Not supported |
| Model support | `deepseek-flash` | `deepseek-flash` | — |

Currently, deferred loading is not available with `deepseek-v4-pro`: the Anthropic API ignores the loading effect of `defer_loading`, `tool_addition`, and `tool_reference` (a `tool_reference` is rendered as plain text) and makes all declared tools available from the start, and the Responses API ignores `tool_search` tool declarations and `tool_search_call` / `tool_search_output` items.

Loaded tools are part of the conversation history. The API is stateless, so replay the history — including the loading record — in every later request. In the Anthropic API, keep the deferred tool declared in the top-level `tools` array with `defer_loading: true` as well. A loaded tool remains available for the rest of the conversation.

Deferred loading also keeps the context cache effective. Deferred tool definitions are left out of the leading system prompt, and loading a tool appends its schema after the existing history instead of rewriting the beginning of the request, so previously cached prefixes stay valid and only the appended part is new input (a cache miss). In contrast, changing the set of non-deferred tools in the top-level `tools` array changes the leading prompt and can prevent the previous cached prefix from matching. See [Context Caching](kv_cache.md).

### Anthropic API

Mark the tools to defer with `defer_loading: true` in the top-level `tools` array. Deferred tools are declared but not shown to the model initially; at least one tool in the request must not be deferred.

On models whose `system_prompt_update` is `in-history` (see the [List Models API](../api/list-models.md#responses)), a mid-conversation `system` message updates the effective system prompt; when instructions conflict, later `system` messages take precedence over earlier ones (earlier messages remain in the history, and non-conflicting instructions can still apply). See [Mid-conversation system messages](anthropic_api.md#mid-conversation-system-messages).

A deferred tool is loaded when a `tool_reference` block naming it appears in either of these places:

- the `content` of a `tool_result` block in a `user` message;
- the `tool` field of a `tool_addition` block in a mid-conversation `system` message.

For the `tool_result` path, the client usually provides a normal tool, such as `search_tools`, that the model calls with a query. The deferred tool schemas are still invisible, so the model needs another way to learn what it can load: describe the catalog in the search tool's description, or add a system message that lists the available deferred tools. When the model calls `search_tools`, append that assistant `tool_use` block and your `tool_result` to the history in the next request, and return the matching tools as `tool_reference` blocks:

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
    {"role": "user", "content": "What's the weather in Hangzhou?"},
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

`get_weather` is loaded at that point in the history, so the model can call it in the same response:

```json
{
  "stop_reason": "tool_use",
  "content": [
    {"type": "tool_use", "id": "toolu_2", "name": "get_weather", "input": {"city": "Hangzhou"}}
  ]
}
```

To load a tool without a model-generated search call, put a `tool_addition` block in a mid-conversation `system` message instead:

```json
{
  "role": "system",
  "content": [
    {"type": "tool_addition", "tool": {"type": "tool_reference", "name": "get_weather"}}
  ]
}
```

Loading is addition-only. Every tool referenced by a `tool_addition` block or a `tool_reference` block must be declared in the top-level `tools` array. `tool_removal` and inline `tool_definition` blocks are not supported. Deferred loading cannot be combined with `deepseek_web_search` or `deepseek_read_url`.

### Responses API

In the Responses API format, functions declared in the top-level `tools` array are available from the start, and additional tools are added mid-conversation through `tool_search`. Send a request with a client-executed `tool_search` tool in `tools`; its `description` and `parameters` tell the model when to search and what arguments to pass. This example disables thinking so that the follow-up request does not have to pass reasoning items back:

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
  "input": "What's the weather in Hangzhou?"
}
```

When the model needs a tool, it returns a `tool_search_call` output item. `tsc_1` and `call_1` below are placeholders for the item `id` and `call_id`:

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

The application searches its catalog and sends a new request. The request repeats the original input and the `tool_search_call` item, and adds a `tool_search_output` item with the same `call_id` and the full definitions of the matched tools in its own `tools` field. Only `type`, `call_id`, `execution`, and `arguments` need to be passed back for the `tool_search_call` item:

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
    {"role": "user", "content": "What's the weather in Hangzhou?"},
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

The tools in `tool_search_output.tools` are available from that point in the input. The model can call them like normal function tools; return each result as a `function_call_output` item and continue the conversation. Only `execution: "client"` is supported — the service does not search for tools on the server. `tool_search` cannot be combined with `deepseek_web_search` or `deepseek_read_url`.

With thinking enabled, pass back the model's `reasoning` output items as well, or reuse the exact `call_id` returned by the API so the service can recover the reasoning.

### Chat Completion API

The Chat Completion API has no deferred loading. Every tool in `tools` is available to the model from the start of the request. To change the available tools, send the complete new `tools` array with the next request; the conversation history does not record tool definitions.

---

## Inserting Tool Calls Mid-Conversation

In some agent scenarios, the client needs to insert a tool call that was not generated by the model — together with its result — into the middle of the conversation history. All three API formats accept such a history, but the required shape differs:

- **Anthropic API**: an assistant message containing `tool_use` blocks must be followed immediately by a `user` message whose first blocks are `tool_result` blocks, one for each `tool_use` ID.
- **Responses API**: a `function_call` input item must be followed by a `function_call_output` item with the same `call_id` before any other message item. Outputs for a group of calls may appear in any order.
- **Chat Completion API**: an assistant message with `tool_calls` must be followed immediately by one `tool` message per call, with matching `tool_call_id` values. The API validates the pairing and rejects duplicate IDs, but does not verify that the calls were generated by the model or that the tools are declared in `tools`.

Inserting a call does not declare or load a tool. In the Anthropic and Responses APIs, use the deferred-loading mechanisms above if the tool definition is not already available in the conversation. In the Chat Completion API, the model can call a tool only if it is present in the top-level `tools` array; inserting a call does not add it.

### Inserting System Messages Mid-Conversation

All three API formats support `system` messages in the middle of the conversation: Anthropic and Chat Completion use a message with `role: "system"`, and the Responses API uses a `message` item with role `system`. A system message cannot split a tool call from its results.

---

## `strict` Mode (Beta)

In `strict` mode, the model strictly adheres to the format requirements of the Function's JSON schema when outputting a tool call, ensuring that the model's output complies with the user's definition. It is supported by both thinking and non-thinking mode.

To use `strict` mode, you need to:：

1. Use `base_url="https://api.deepseek.com/beta"` to enable Beta features
2. In the `tools` parameter，all `function` need to set the `strict` property to `true`
3. The server will validate the JSON Schema of the Function provided by the user. If the schema does not conform to the specifications or contains JSON schema types that are not supported by the server, an error message will be returned

The following is an example of a tool definition in the `strict` mode:

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

### Support Json Schema Types In `strict` Mode

- object
- string
- number
- integer
- boolean
- array
- enum
- anyOf

---

#### object

The `object` defines a nested structure containing key-value pairs, where `properties` specifies the schema for each key (or property) within the object. **All properties of every `object` must be set as `required`, and the `additionalProperties` attribute of the `object` must be set to `false`.**

Example：

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

#### string

- Supported parameters:

  - `pattern`: Uses regular expressions to constrain the format of the string
  - `format`: Validates the string against predefined common formats. Currently supported formats:
    - `email`: Email address
    - `hostname`: Hostname
    - `ipv4`: IPv4 address
    - `ipv6`: IPv6 address
    - `uuid`: UUID
- Unsupported parameters:

  - `minLength`
  - `maxLength`

Example:

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

#### number/integer

- Supported parameters:
  - `const`: Specifies a constant numeric value
  - `default`: Defines the default value of the number
  - `minimum`: Specifies the minimum value
  - `maximum`: Specifies the maximum value
  - `exclusiveMinimum`: Defines a value that the number must be greater than
  - `exclusiveMaximum`: Defines a value that the number must be less than
  - `multipleOf`: Ensures that the number is a multiple of the specified value

Example:

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

#### array

- Unsupported parameters:
  - minItems
  - maxItems

Example：

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

The `enum` ensures that the output is one of the predefined options. For example, in the case of order status, it can only be one of a limited set of specified states.

Example：

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

Matches any one of the provided schemas, allowing fields to accommodate multiple valid formats. For example, a user's account could be either an email address or a phone number:

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

#### $ref and $def

You can use `$def` to define reusable modules and then use `$ref` to reference them, reducing schema repetition and enabling modularization. Additionally, `$ref` can be used independently to define recursive structures.

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
