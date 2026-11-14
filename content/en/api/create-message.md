---
title: "Messages API"
description: "Creates a model response in the Anthropic Messages API format."
source: https://api-docs.deepseek.com/api/create-message
fetched: 2026-11-14
---

# Messages API

[Open Markdown](https://api-docs.deepseek.com/api/create-message.md "Open Markdown in a new tab")

```
POST /anthropic/v1/messages
```

Creates a model response in the Anthropic Messages API format.

Send the conversation history in `messages` on each request. Use `https://api.deepseek.com/anthropic` as the Anthropic SDK's `base_url`; the SDK appends `/v1/messages`. Direct HTTP requests can also use the compatible path `/anthropic/messages`.

Authenticate with either `x-api-key` or `Authorization: Bearer`. If both are supplied, `Authorization` takes precedence. See the [Anthropic API Guide](../guides/anthropic_api.md) for model mappings, tool-result replay, and compatibility details.

Compatibility fields `container`, `mcp_servers`, `service_tier`, and `top_k` are ignored.

## Request

**Header Parameters**

**anthropic-version** string

The Anthropic SDK sends this header automatically; the service currently ignores it.

**Example:** 2023-06-01

**anthropic-beta** string

Include `files-api-2025-04-14` when referencing an uploaded image with `source.type` of `file`. Otherwise not required for this endpoint. See the [Files API Guide](../guides/files_api.md#anthropic-compatible-files-api).

**Example:** files-api-2025-04-14

**[application/json]**

**Bodyrequired**

**model** stringrequired

ID of the model to use. Use `deepseek-flash` or `deepseek-v4-pro`. Claude model-name aliases are also accepted: `claude-opus*` maps to `deepseek-v4-pro`, and other `claude*` names map to `deepseek-flash`. See the [Anthropic API Guide](../guides/anthropic_api.md).

**messages**

object[]

required

**Minimum items:** `1`

The conversation history. At least one message is required. This API is stateless: include the messages needed for the current turn in every request. Use the top-level `system` field for the system prompt. When continuing after a tool call, pass back the complete assistant content, including thinking and tool-use blocks, followed by the matching tool results. The service may restore omitted thinking content from tool-call IDs; if recovery is required but fails, the request returns `400`. Preserve the complete content for reliable replay.

- Array [

oneOf

- User message
- Assistant message
- Latest reminder message

**[User message]**

**role** stringrequired

**Possible values:** `user`

**content** string | object[]

required

oneOf

- Text content
- User content blocks

**[Assistant message]**

string

**[Latest reminder message]**

**Minimum items:** `1`

Place all `tool_result` blocks before text or image blocks when replying to tool calls.

- Array [

oneOf

- Text block
- Image block
- Document block
- Tool-result block

**[Text content]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[User content blocks]**

Image input is supported by `deepseek-flash` in user messages and tool results. Images in assistant messages are not supported. `deepseek-v4-pro` does not support image input. See the [Vision Guide](../guides/vision.md) for image limits.

**type** stringrequired

**Possible values:** `image`

**source** object

required

oneOf

- Base64 image
- Image URL
- Uploaded image file

**[Text block]**

**type** stringrequired

**Possible values:** `base64`

**media\_type** stringrequired

**Possible values:** `image/jpeg`, `image/png`, `image/gif`, `image/webp`

**data** stringrequired

The base64-encoded image bytes, without a data-URL prefix.

**[Image block]**

**type** stringrequired

**Possible values:** `url`

**url** urirequired

An HTTP or HTTPS URL from which the server can download the image.

**[Document block]**

Requires the request header `anthropic-beta: files-api-2025-04-14`.

**type** stringrequired

**Possible values:** `file`

**file\_id** stringrequired

The ID of an uploaded image file. See the [Files API Guide](../guides/files_api.md#anthropic-compatible-files-api).

**[Tool-result block]**

A document for the model to read, supported in user messages. See the [File Parsing Guide](../guides/document_parsing.md#document-qa).

**type** stringrequired

**Possible values:** `document`

**source** object

required

oneOf

- Uploaded file
- Inline text

**[Base64 image]**

The request must carry the `anthropic-beta: files-api-2025-04-14` header.

**type** stringrequired

**Possible values:** `file`

**file\_id** stringrequired

The ID of a file uploaded via the [Files API](../guides/files_api.md), of the form `file-api-...`.

**[Image URL]**

**type** stringrequired

**Possible values:** `text`

**media\_type** string

**Possible values:** `text/plain`

**data** stringrequired

The text of the document.

**title** string

Optional. The file name shown to the model for a `text` source.

**[Uploaded image file]**

Only valid in user messages. Return one result for every pending tool-use ID, with no duplicates, before any text or image blocks.

**type** stringrequired

**Possible values:** `tool_result`

**tool\_use\_id** stringrequired

The ID of the corresponding `tool_use` block in the immediately preceding assistant message.

**content** string | object[] | null

nullable

The tool output as a string or a list of text and image blocks. If omitted or `null`, the result is empty.

oneOf

- Text content
- Tool-result content blocks
- Null value

**[Uploaded file]**

string

**[Inline text]**

- Array [

oneOf

- Text block
- Image block

**[Text content]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[Tool-result content blocks]**

Image input is supported by `deepseek-flash` in user messages and tool results. Images in assistant messages are not supported. `deepseek-v4-pro` does not support image input. See the [Vision Guide](../guides/vision.md) for image limits.

**type** stringrequired

**Possible values:** `image`

**source** object

required

oneOf

- Base64 image
- Image URL
- Uploaded image file

**[Null value]**

**type** stringrequired

**Possible values:** `base64`

**media\_type** stringrequired

**Possible values:** `image/jpeg`, `image/png`, `image/gif`, `image/webp`

**data** stringrequired

The base64-encoded image bytes, without a data-URL prefix.

**[Text block]**

**type** stringrequired

**Possible values:** `url`

**url** urirequired

An HTTP or HTTPS URL from which the server can download the image.

**[Image block]**

Requires the request header `anthropic-beta: files-api-2025-04-14`.

**type** stringrequired

**Possible values:** `file`

**file\_id** stringrequired

The ID of an uploaded image file. See the [Files API Guide](../guides/files_api.md#anthropic-compatible-files-api).

- ]

**[Base64 image]**

null

**is\_error** booleannullable

Ignored. Include any error details in `content`.

- ]

**[Image URL]**

A previous assistant message. Preserve its content blocks when passing it back, including thinking, tool use, and web search results.

**role** stringrequired

**Possible values:** `assistant`

**content** string | object[]

required

oneOf

- Text content
- Assistant content blocks

**[Uploaded image file]**

string

**[Text content]**

**Minimum items:** `1`

- Array [

oneOf

- Text block
- Thinking block
- Tool-use block
- Server-tool-use block
- Web search result block
- Web fetch result block

**[Assistant content blocks]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[Text block]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

Thinking content returned by the model. Pass it back unchanged when continuing a tool-call turn in thinking mode.

**signature** stringnullable

The signature returned with the thinking block. Preserve it when passing back the block; the input signature is not validated.

**[Thinking block]**

Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

The tool-call ID. Pass this ID back as `tool_result.tool_use_id`.

**name** stringrequired

The name of the client tool.

**input** nullablerequired

The JSON arguments supplied to the tool, normally an object matching its `input_schema`.

**[Tool-use block]**

Returned when the service runs web search, `deepseek_web_search` or `deepseek_read_url`. Its matching `web_search_tool_result` or `web_fetch_tool_result` appears in the same assistant message; the client does not run this tool.

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

The server-tool-call ID.

**name** stringrequired

**Possible values:** `web_search`, `web_fetch`, `deepseek_web_search`, `deepseek_read_url`

**input** nullablerequired

The server-tool arguments as a JSON value, normally an object such as `{"query":"..."}`. Preserve them when passing back the assistant message.

**caller**

object

Identifies a direct server-tool call.

**type** stringrequired

**Possible values:** `direct`

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Server-tool-use block]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content**

object[]

required

Search results or search-error items. Pass the entire array back unchanged with the assistant message.

- Array [

oneOf

- Web search result
- Web search error

**[Web search result block]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

The title of the result page.

**url** urirequired

The URL of the result page.

**encrypted\_content** stringrequired

Opaque result content. Preserve this value unchanged when passing the result back.

**page\_age** stringnullable

Page-age metadata, when available; may be `null`.

**snippet** stringnullable

DeepSeek extension. A plain-text summary of the result for display.

**site\_name** stringnullable

DeepSeek extension. The name of the site, or `null` when unknown.

**site\_icon** stringnullable

DeepSeek extension. The URL of the site icon, or `null` when unknown.

**[Web fetch result block]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

The reason the server-side search failed.

- ]

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Web search result]**

Returned for a page opened during deep thinking search (`deepseek_web_search`), or a link read by `deepseek_read_url`. Pass it back unchanged, including `kind` and `signature`. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**type** stringrequired

**Possible values:** `web_fetch_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content** object

required

The fetched page, or the reason the fetch failed.

oneOf

- Web fetch result
- Web fetch error

**[Web search error]**

**type** stringrequired

**Possible values:** `web_fetch_result`

**url** stringrequired

The URL of the page.

**content**

object

required

The page as a text document.

**type** string

**Possible values:** `document`

**source**

object

**type** string

**Possible values:** `text`

**media\_type** string

**Possible values:** `text/plain`

**data** string

Always an empty string: the page text is not returned. For `read_link`, the page is carried in `signature`.

**title** stringnullable

The page title.

**published\_at** stringnullable

DeepSeek extension, in place of `retrieved_at`. The publication time of the page, or `null` when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.

**[Web fetch result]**

**type** stringrequired

**Possible values:** `web_fetch_tool_result_error`

**error\_code** stringrequired

**Possible values:** `url_not_accessible`, `url_not_allowed`, `unavailable`

The reason the fetch failed. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**signature** string

DeepSeek extension. Present on successful `read_link` results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.

- ]

**[Web fetch error]**

DeepSeek extension. Gives the model the current date, location, platform and language, like DeepSeek Chat. Place it directly before the `user` message it belongs to; anywhere else it returns `400`. Works with or without the web tools. See the [User Metadata Marker Guide](../guides/latest_reminder.md).

**role** stringrequired

**Possible values:** `latest_reminder`

**content** stringrequired

`<date>,<weekday>,<location>,<platform>,<language>`, for example `2026-11-11,Wednesday,Singapore,Web,English`.

- ]

**system** string | object[] | null

nullable

The system prompt. Supports only a string, an array of text blocks, or `null`.

oneOf

- Text content
- System text blocks
- Null value

**[Text content]**

string

**[System text blocks]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

- Array [

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

- ]

**[Null value]**

null

**max\_tokens** integernullable

**Possible values:** `>= 1`

The requested output token limit, including thinking tokens. This field is optional at the HTTP API level; the Anthropic SDK requires it. The default and effective limit depend on the model, thinking mode, and reasoning effort. Values above the model limit are capped, and the input plus output must fit within the context window. For certain Claude Code or OpenCode main-agent requests in thinking mode, compatibility handling may raise the effective limit above the requested value, within model and context limits. See [Models & Pricing](../quick_start/pricing.md).

**stream** booleannullable

**Default value:** `false`

If `true`, return named server-sent events (SSE), ending with `message_stop`. There is no `data: [DONE]` message. Otherwise, return one complete message object.

**thinking**

object

nullable

Controls thinking mode. An explicit `thinking.type` takes precedence over `output_config.effort` when selecting the mode. When omitted, `effort` determines the mode. If neither is set, thinking is enabled by default for `deepseek-flash` and `deepseek-v4-pro`.

**type** stringrequired

**Possible values:** `enabled`, `disabled`, `adaptive`

`enabled` turns thinking on; `disabled` turns it off. `adaptive` is treated as `enabled`.

**budget\_tokens** integernullable

**Possible values:** `>= 0`

Ignored. This parameter does not set a thinking-token budget.

**output\_config**

object

nullable

Output configuration. Only `effort` is supported; output-format settings such as `format` are ignored.

**effort** stringnullable

**Possible values:** `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `ultra`, `max`, `null`

Controls thinking mode and effort. `none` disables thinking unless `thinking.type` explicitly enables it. `low`, `high`, and `max` enable thinking, with `high` as the default effort. Compatibility aliases: `minimal` maps to `low`, `medium` and `xhigh` both map to `high`, and `ultra` maps to `max`. An explicit `thinking.type` determines whether thinking is enabled.

**tools**

object[]

nullable

Tools available to the model. Supports client-defined tools, the web search server tool, and the `deepseek_web_search` and `deepseek_read_url` server tools. Tool names must be unique. An empty list is treated as no tools. `cache_control` is ignored.

- Array [

oneOf

- Client tool
- Web search server tool
- DeepSeek web search server tool
- DeepSeek read URL server tool

**[Client tool]**

The application executes this tool after receiving a `tool_use` block and returns a `tool_result` block. Omit `type` for client tools. Providing `type` selects server-tool parsing; unsupported values such as `custom` return `422`. `cache_control` is ignored.

**name** stringrequired

**Minimum characters:** `1`

**Maximum characters:** `128`

**Possible values:** Value must match regular expression `^[a-zA-Z0-9_-]+$`

A unique tool name containing letters, digits, underscores, or hyphens, up to 128 characters.

**description** stringnullable

A description of what the tool does and when to use it.

**input\_schema**

object

required

A valid JSON Schema describing the tool arguments. Its top-level `type` must be `object`.

**property name\*** anynullable

**[Web search server tool]**

The service executes web searches and returns `server_tool_use` and `web_search_tool_result` blocks in the assistant message. Both type values select the same tool.

**type** stringrequired

**Possible values:** `web_search_20250305`, `web_search_20260209`

**name** stringrequired

**Possible values:** `web_search`

**max\_uses** integernullable

**Possible values:** `>= 0`

Maximum searches allowed in this request. The default and service-side cap are normally 5; for Claude Code search-subagent compatibility requests, both are 1. Larger values are capped at the applicable limit. A search beyond this limit returns a `max_uses_exceeded` result.

**[DeepSeek web search server tool]**

DeepSeek extension. Lets the model search the web; with thinking enabled, it runs deep thinking search. See the [Web Tools Guide](../guides/web_tools.md).

**type** stringrequired

**Possible values:** `deepseek_web_search`

**name** string

**Possible values:** `deepseek_web_search`

Optional. The service does not check it.

**[DeepSeek read URL server tool]**

DeepSeek extension. Lets the model read the links in the last user message. See the [Web Tools Guide](../guides/web_tools.md#read-links).

**type** stringrequired

**Possible values:** `deepseek_read_url`

**name** string

**Possible values:** `deepseek_read_url`

Optional. The service does not check it.

- ]

**tool\_choice** object | null

nullable

Controls tool selection. Defaults to `auto`. `any` is treated as `auto` and does not force a tool call. Selecting a named client tool requires non-thinking mode. `disable_parallel_tool_use` is ignored.

oneOf

- Automatic tool choice
- Any tool (automatic)
- Named tool choice
- Disable tool calls
- Null value

**[Automatic tool choice]**

The model decides whether to call a tool. This is the default.

**type** stringrequired

**Possible values:** `auto`

**disable\_parallel\_tool\_use** booleannullable

Ignored; it does not disable parallel tool calls.

**[Any tool (automatic)]**

Treated as `auto`; the model decides whether to call a tool.

**type** stringrequired

**Possible values:** `any`

**disable\_parallel\_tool\_use** booleannullable

Ignored; it does not disable parallel tool calls.

**[Named tool choice]**

Selects the named tool. For a client tool, this forces a call in non-thinking mode; selecting it in thinking mode returns a `400` error. Set `thinking.type` to `disabled` when forcing a client-tool call.

**type** stringrequired

**Possible values:** `tool`

**name** stringrequired

The name of a tool present in `tools`.

**disable\_parallel\_tool\_use** booleannullable

Ignored; it does not disable parallel tool calls.

**[Disable tool calls]**

Disables tool calling, even when `tools` is provided.

**type** stringrequired

**Possible values:** `none`

**[Null value]**

null

**stop\_sequences** string[]nullable

**Minimum characters per item:** `1`

**Maximum items:** `16`

Up to 16 non-empty strings that stop generation. If a string is matched, `stop_reason` is `stop_sequence` and `stop_sequence` contains the matched string.

**temperature** numbernullable

**Possible values:** `>= 0` and `<= 2`

**Default value:** `1`

Sampling temperature, between 0 and 2. Higher values produce more varied output. In thinking mode the value is fixed at 1, and the supplied value has no effect. We generally recommend changing either this or `top_p`, rather than both.

**top\_p** numbernullable

**Possible values:** `> 0` and `<= 1`

Nucleus sampling probability, greater than 0 and at most 1. For `deepseek-flash`, thinking mode defaults to 1 and clamps values below 0.95 to 0.95; non-thinking mode always uses 1. For `deepseek-v4-pro`, thinking mode uses 0.95 when tools are enabled and 1 otherwise, ignoring the supplied value; non-thinking mode uses the supplied value, defaulting to 1. Setting `tool_choice` to `{"type":"none"}` disables tool calling.

**metadata**

object

nullable

Request metadata. Only `user_id` is supported; other metadata fields are ignored.

**user\_id** stringnullable

A custom end-user identifier. We recommend using only ASCII letters, digits, underscores (`_`), and hyphens (`-`). The UTF-8 encoded value must not exceed 512 bytes. Do not include personal information. See [Rate Limit & Isolation](../quick_start/rate_limit.md).

**safety\_check**

object

nullable

DeepSeek extension. Set `level` to `high` to turn on basic risk control, which reviews the model input and output. See the [Model Content Safety Guide](../guides/safety.md).

**level** stringrequired

**Possible values:** `low`, `high`

`high`: basic risk control. `low`: the default checks, the same as omitting `safety_check`.

**title**

object

nullable

DeepSeek extension. Set `{"enabled": true}` to have the response carry a short title for the conversation. See the [Conversation Title Guide](../guides/conversation_title.md).

**enabled** booleanrequired

Whether to return a conversation title.

## Responses

- 200 (No streaming)
- 200 (Streaming)
- 400 (Bad request)

OK, returns a `message` object. Its content may include text, thinking, and tool-use blocks.

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**id** stringrequired

Unique identifier for this message.

**type** stringrequired

**Possible values:** `message`

**role** stringrequired

**Possible values:** `assistant`

**model** stringrequired

The model identifier supplied in the request. When using a Claude-compatible model name, the response retains that name.

**content**

object[]

required

Generated content blocks. Preserve the full content when adding this assistant turn to the next request.

- Array [

oneOf

- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block

**[Example]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[Text block]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.

**signature** stringrequired

Opaque signature returned with the thinking block; preserve it when replaying the block.

**[Thinking output]**

Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

The tool-call ID. Pass this ID back as `tool_result.tool_use_id`.

**name** stringrequired

The name of the client tool.

**input** nullablerequired

The JSON arguments supplied to the tool, normally an object matching its `input_schema`.

**[Tool-use block]**

Describes a tool call executed by the service. Request-level search counts are reported separately in `usage.server_tool_use`; the client does not execute this call.

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

Identifier of the server tool call.

**name** stringrequired

Name of the server tool: `web_search` for web search. With the web tools, the declared tool that enabled the capability: `deepseek_web_search` for searches and the steps of deep thinking search, or `deepseek_read_url` for URL reading.

**input** nullablerequired

Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, `input.action` is `search`, `open_page`, `find_in_page` or `read_link`.

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Server tool use output]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content**

object[]

required

Search results or search-error items. Pass the entire array back unchanged with the assistant message.

- Array [

oneOf

- Web search result
- Web search error

**[Web search result block]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

The title of the result page.

**url** urirequired

The URL of the result page.

**encrypted\_content** stringrequired

Opaque result content. Preserve this value unchanged when passing the result back.

**page\_age** stringnullable

Page-age metadata, when available; may be `null`.

**snippet** stringnullable

DeepSeek extension. A plain-text summary of the result for display.

**site\_name** stringnullable

DeepSeek extension. The name of the site, or `null` when unknown.

**site\_icon** stringnullable

DeepSeek extension. The URL of the site icon, or `null` when unknown.

**[Web fetch result block]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

The reason the server-side search failed.

- ]

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Web search result]**

Returned for a page opened during deep thinking search (`deepseek_web_search`), or a link read by `deepseek_read_url`. Pass it back unchanged, including `kind` and `signature`. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**type** stringrequired

**Possible values:** `web_fetch_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content** object

required

The fetched page, or the reason the fetch failed.

oneOf

- Web fetch result
- Web fetch error

**[Web search error]**

**type** stringrequired

**Possible values:** `web_fetch_result`

**url** stringrequired

The URL of the page.

**content**

object

required

The page as a text document.

**type** string

**Possible values:** `document`

**source**

object

**type** string

**Possible values:** `text`

**media\_type** string

**Possible values:** `text/plain`

**data** string

Always an empty string: the page text is not returned. For `read_link`, the page is carried in `signature`.

**title** stringnullable

The page title.

**published\_at** stringnullable

DeepSeek extension, in place of `retrieved_at`. The publication time of the page, or `null` when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.

**[Web fetch result]**

**type** stringrequired

**Possible values:** `web_fetch_tool_result_error`

**error\_code** stringrequired

**Possible values:** `url_not_accessible`, `url_not_allowed`, `unavailable`

The reason the fetch failed. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**signature** string

DeepSeek extension. Present on successful `read_link` results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.

- ]

**stop\_reason** stringnullablerequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`, `null`

Why generation stopped: natural completion, output limit, a stop sequence, a client tool call, or content filtering. Null in message\_start.

**stop\_sequence** stringnullablerequired

The matched stop sequence, or null when no stop sequence was matched.

**stop\_details**

object

nullable

Present when the model content safety review refuses the response (`stop_reason` is `refusal`). See the [Model Content Safety Guide](../guides/safety.md#handling-refusals).

**type** stringrequired

**Possible values:** `refusal`

**category** stringnullable

Always `null`.

**explanation** stringnullable

Names the blocked images when images in the request fail the review; otherwise `null`.

**title** string

DeepSeek extension. The conversation title, present only when the request enabled `title` and a title was generated. Not related to the `title` of search results and citations.

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens not served from the context cache. Total input tokens equal input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens.

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

Always 0. Anthropic-style cache creation is not used; context caching is automatic.

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens served from the context cache.

**output\_tokens** integerrequired

**Possible values:** `>= 0`

Generated output tokens, including thinking tokens when thinking is enabled. In message\_delta this is the cumulative count, not an increment.

**output\_tokens\_details**

object

Breakdown of `output_tokens`. Present when thinking is enabled or `safety_check` is `high`.

**thinking\_tokens** integer

**Possible values:** `>= 0`

Thinking tokens, already included in `output_tokens`.

**safety\_tokens** integer

**Possible values:** `>= 0`

DeepSeek extension. Tokens of the safety review, already included in `output_tokens`. Present only when `safety_check` is `high`.

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message\_delta.usage for streaming responses. These counts are cumulative, not deltas. See [Server tool usage](../guides/anthropic_api.md#server-tool-usage).

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

Number of server-side web search attempts, including failed attempts and attempts exceeding `max_uses`.

**tool\_search** integerrequired

**Possible values:** `>= 0`

Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.

**web\_fetch\_requests** integer

**Possible values:** `>= 0`

With the web tools. Number of fetch result blocks in the response, including errors. For display only.

**tool\_fetch** integer

**Possible values:** `>= 0`

With the web tools. Number of billed page fetches.

**tool\_image\_search** integer

**Possible values:** `>= 0`

With the web tools. Number of billed image searches.

**[Web fetch error]**

```json
{
  "id": "e6ef6a63-a078-4f53-a73b-38c8d1d46310",
  "type": "message",
  "role": "assistant",
  "model": "deepseek-flash",
  "content": [{"type": "text", "text": "Hello!"}],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 3,
    "service_tier": "standard"
  }
}
```

OK, returns SSE events in the order `message_start` → content block events → `message_delta` → `message_stop`. A `ping` event or keep-alive comment may appear between events. There is no `data: [DONE]` message. Accumulate tool input JSON fragments until the content block ends before parsing them. See [Streaming](../guides/anthropic_api.md#streaming).

A connection that closes before `message_stop` is an incomplete response. Errors after streaming has started may terminate the connection without an Anthropic `error` event.

**[text/event-stream]**

- Schema
- Example

**[Schema]**

**Schema**

Normal message events have an event name matching the JSON type. A normal stream ends with message\_stop. Ping events and keep-alive comments may appear between events; no data: [DONE] is emitted. A timeout may instead return an unnamed data event containing an error object before closing the connection. An interrupted stream without message\_stop is incomplete.

- Array [

oneOf

- message\_start
- content\_block\_start
- content\_block\_delta
- content\_block\_stop
- message\_delta
- message\_stop
- ping

**[Example]**

**type** stringrequired

**Possible values:** `message_start`

**message**

object

required

**id** stringrequired

Unique identifier for this message.

**type** stringrequired

**Possible values:** `message`

**role** stringrequired

**Possible values:** `assistant`

**model** stringrequired

The model identifier supplied in the request. When using a Claude-compatible model name, the response retains that name.

**content**

object[]

required

Generated content blocks. Preserve the full content when adding this assistant turn to the next request.

- Array [

oneOf

- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block

**[message\_start]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[content\_block\_start]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.

**signature** stringrequired

Opaque signature returned with the thinking block; preserve it when replaying the block.

**[content\_block\_delta]**

Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

The tool-call ID. Pass this ID back as `tool_result.tool_use_id`.

**name** stringrequired

The name of the client tool.

**input** nullablerequired

The JSON arguments supplied to the tool, normally an object matching its `input_schema`.

**[content\_block\_stop]**

Describes a tool call executed by the service. Request-level search counts are reported separately in `usage.server_tool_use`; the client does not execute this call.

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

Identifier of the server tool call.

**name** stringrequired

Name of the server tool: `web_search` for web search. With the web tools, the declared tool that enabled the capability: `deepseek_web_search` for searches and the steps of deep thinking search, or `deepseek_read_url` for URL reading.

**input** nullablerequired

Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, `input.action` is `search`, `open_page`, `find_in_page` or `read_link`.

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[message\_delta]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content**

object[]

required

Search results or search-error items. Pass the entire array back unchanged with the assistant message.

- Array [

oneOf

- Web search result
- Web search error

**[message\_stop]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

The title of the result page.

**url** urirequired

The URL of the result page.

**encrypted\_content** stringrequired

Opaque result content. Preserve this value unchanged when passing the result back.

**page\_age** stringnullable

Page-age metadata, when available; may be `null`.

**snippet** stringnullable

DeepSeek extension. A plain-text summary of the result for display.

**site\_name** stringnullable

DeepSeek extension. The name of the site, or `null` when unknown.

**site\_icon** stringnullable

DeepSeek extension. The URL of the site icon, or `null` when unknown.

**[ping]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

The reason the server-side search failed.

- ]

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Text block]**

Returned for a page opened during deep thinking search (`deepseek_web_search`), or a link read by `deepseek_read_url`. Pass it back unchanged, including `kind` and `signature`. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**type** stringrequired

**Possible values:** `web_fetch_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content** object

required

The fetched page, or the reason the fetch failed.

oneOf

- Web fetch result
- Web fetch error

**[Thinking output]**

**type** stringrequired

**Possible values:** `web_fetch_result`

**url** stringrequired

The URL of the page.

**content**

object

required

The page as a text document.

**type** string

**Possible values:** `document`

**source**

object

**type** string

**Possible values:** `text`

**media\_type** string

**Possible values:** `text/plain`

**data** string

Always an empty string: the page text is not returned. For `read_link`, the page is carried in `signature`.

**title** stringnullable

The page title.

**published\_at** stringnullable

DeepSeek extension, in place of `retrieved_at`. The publication time of the page, or `null` when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.

**[Tool-use block]**

**type** stringrequired

**Possible values:** `web_fetch_tool_result_error`

**error\_code** stringrequired

**Possible values:** `url_not_accessible`, `url_not_allowed`, `unavailable`

The reason the fetch failed. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**signature** string

DeepSeek extension. Present on successful `read_link` results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.

- ]

**stop\_reason** stringnullablerequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`, `null`

Why generation stopped: natural completion, output limit, a stop sequence, a client tool call, or content filtering. Null in message\_start.

**stop\_sequence** stringnullablerequired

The matched stop sequence, or null when no stop sequence was matched.

**stop\_details**

object

nullable

Present when the model content safety review refuses the response (`stop_reason` is `refusal`). See the [Model Content Safety Guide](../guides/safety.md#handling-refusals).

**type** stringrequired

**Possible values:** `refusal`

**category** stringnullable

Always `null`.

**explanation** stringnullable

Names the blocked images when images in the request fail the review; otherwise `null`.

**title** string

DeepSeek extension. The conversation title, present only when the request enabled `title` and a title was generated. Not related to the `title` of search results and citations.

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens not served from the context cache. Total input tokens equal input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens.

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

Always 0. Anthropic-style cache creation is not used; context caching is automatic.

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens served from the context cache.

**output\_tokens** integerrequired

**Possible values:** `>= 0`

Generated output tokens, including thinking tokens when thinking is enabled. In message\_delta this is the cumulative count, not an increment.

**output\_tokens\_details**

object

Breakdown of `output_tokens`. Present when thinking is enabled or `safety_check` is `high`.

**thinking\_tokens** integer

**Possible values:** `>= 0`

Thinking tokens, already included in `output_tokens`.

**safety\_tokens** integer

**Possible values:** `>= 0`

DeepSeek extension. Tokens of the safety review, already included in `output_tokens`. Present only when `safety_check` is `high`.

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message\_delta.usage for streaming responses. These counts are cumulative, not deltas. See [Server tool usage](../guides/anthropic_api.md#server-tool-usage).

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

Number of server-side web search attempts, including failed attempts and attempts exceeding `max_uses`.

**tool\_search** integerrequired

**Possible values:** `>= 0`

Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.

**web\_fetch\_requests** integer

**Possible values:** `>= 0`

With the web tools. Number of fetch result blocks in the response, including errors. For display only.

**tool\_fetch** integer

**Possible values:** `>= 0`

With the web tools. Number of billed page fetches.

**tool\_image\_search** integer

**Possible values:** `>= 0`

With the web tools. Number of billed image searches.

**[Server tool use output]**

**type** stringrequired

**Possible values:** `content_block_start`

**index** integerrequired

**Possible values:** `>= 0`

Zero-based index of the content block.

**content\_block** object

required

oneOf

- Text block
- Thinking output
- Tool-use block
- Server tool use output
- Web search result block
- Web fetch result block

**[Web search result block]**

Each text block must have `type: "text"`, with its content in the `text` field. On input, additional `cache_control` and `citations` fields are ignored.

**type** stringrequired

**Possible values:** `text`

**text** stringrequired

The text content.

**citations**

object[]

nullable

Sources cited by this text. Returned when the answer cites results of the web tools; ignored on input.

A source cited by the answer. Returned with the web tools.

- Array [

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

- ]

**[Web fetch result block]**

**type** stringrequired

**Possible values:** `thinking`

**thinking** stringrequired

The generated thinking content. Return this block unchanged when continuing a thinking-mode tool conversation.

**signature** stringrequired

Opaque signature returned with the thinking block; preserve it when replaying the block.

**[Web search result]**

Appears in assistant messages. Each tool-use block must have a matching tool-result block in the immediately following user message.

**type** stringrequired

**Possible values:** `tool_use`

**id** stringrequired

The tool-call ID. Pass this ID back as `tool_result.tool_use_id`.

**name** stringrequired

The name of the client tool.

**input** nullablerequired

The JSON arguments supplied to the tool, normally an object matching its `input_schema`.

**[Web search error]**

Describes a tool call executed by the service. Request-level search counts are reported separately in `usage.server_tool_use`; the client does not execute this call.

**type** stringrequired

**Possible values:** `server_tool_use`

**id** stringrequired

Identifier of the server tool call.

**name** stringrequired

Name of the server tool: `web_search` for web search. With the web tools, the declared tool that enabled the capability: `deepseek_web_search` for searches and the steps of deep thinking search, or `deepseek_read_url` for URL reading.

**input** nullablerequired

Arguments supplied to the server tool as a JSON value, normally an object. With the web tools, `input.action` is `search`, `open_page`, `find_in_page` or `read_link`.

**caller**

object

required

**type** stringrequired

**Possible values:** `direct`

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Web fetch result]**

**type** stringrequired

**Possible values:** `web_search_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content**

object[]

required

Search results or search-error items. Pass the entire array back unchanged with the assistant message.

- Array [

oneOf

- Web search result
- Web search error

**[Web fetch error]**

**type** stringrequired

**Possible values:** `web_search_result`

**title** stringrequired

The title of the result page.

**url** urirequired

The URL of the result page.

**encrypted\_content** stringrequired

Opaque result content. Preserve this value unchanged when passing the result back.

**page\_age** stringnullable

Page-age metadata, when available; may be `null`.

**snippet** stringnullable

DeepSeek extension. A plain-text summary of the result for display.

**site\_name** stringnullable

DeepSeek extension. The name of the site, or `null` when unknown.

**site\_icon** stringnullable

DeepSeek extension. The URL of the site icon, or `null` when unknown.

**[Text block]**

**type** stringrequired

**Possible values:** `web_search_tool_result_error`

**error\_code** stringrequired

**Possible values:** `invalid_tool_input`, `unavailable`, `max_uses_exceeded`, `too_many_requests`, `query_too_long`, `request_too_large`

The reason the server-side search failed.

- ]

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**[Thinking output]**

Returned for a page opened during deep thinking search (`deepseek_web_search`), or a link read by `deepseek_read_url`. Pass it back unchanged, including `kind` and `signature`. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**type** stringrequired

**Possible values:** `web_fetch_tool_result`

**tool\_use\_id** stringrequired

The ID of the associated `server_tool_use` block.

**content** object

required

The fetched page, or the reason the fetch failed.

oneOf

- Web fetch result
- Web fetch error

**[Tool-use block]**

**type** stringrequired

**Possible values:** `web_fetch_result`

**url** stringrequired

The URL of the page.

**content**

object

required

The page as a text document.

**type** string

**Possible values:** `document`

**source**

object

**type** string

**Possible values:** `text`

**media\_type** string

**Possible values:** `text/plain`

**data** string

Always an empty string: the page text is not returned. For `read_link`, the page is carried in `signature`.

**title** stringnullable

The page title.

**published\_at** stringnullable

DeepSeek extension, in place of `retrieved_at`. The publication time of the page, or `null` when unknown. For a link read from the user message, the date found on the page, in no fixed format; for a page opened during deep thinking search, an RFC 3339 timestamp.

**[Server tool use output]**

**type** stringrequired

**Possible values:** `web_fetch_tool_result_error`

**error\_code** stringrequired

**Possible values:** `url_not_accessible`, `url_not_allowed`, `unavailable`

The reason the fetch failed. See the [Web Tools Guide](../guides/web_tools.md#response-blocks).

**kind** Web tools capability (string)

**Possible values:** `search`, `deep_search`, `read_link`, `image_search`, `deep_image_search`

DeepSeek extension on blocks produced by the web tools: `search` for web search, `deep_search` for deep thinking search, `read_link` for URL reading, and `image_search` or `deep_image_search` (during deep thinking search) for image search. Pass it back unchanged.

**signature** string

DeepSeek extension. Present on successful `read_link` results: the page that was read, encrypted. Pass it back unchanged to restore the page into the context.

**[Web search result block]**

**type** stringrequired

**Possible values:** `content_block_delta`

**index** integerrequired

**Possible values:** `>= 0`

Zero-based index of the content block.

**delta** object

required

oneOf

- Text delta
- Thinking delta
- Signature delta
- Tool input delta
- Citations delta

**[Web fetch result block]**

**type** stringrequired

**Possible values:** `text_delta`

**text** stringrequired

Append this text to the current text block.

**[Web search result]**

**type** stringrequired

**Possible values:** `thinking_delta`

**thinking** stringrequired

Append this text to the current thinking block.

**[Web search error]**

**type** stringrequired

**Possible values:** `signature_delta`

**signature** stringrequired

Signature for the completed thinking block.

**[Web fetch result]**

**type** stringrequired

**Possible values:** `input_json_delta`

**partial\_json** stringrequired

A fragment of the tool input JSON. Concatenate all fragments for this block, then parse the JSON after content\_block\_stop.

**[Web fetch error]**

Adds one citation to the current text block. Returned with the web tools.

**type** stringrequired

**Possible values:** `citations_delta`

**citation**

object

required

A source cited by the answer. Returned with the web tools.

**type** stringrequired

**Possible values:** `web_search_result_location`

**url** stringrequired

The URL of the cited source.

**title** stringnullable

The title of the cited source, or `null` when unknown.

**encrypted\_index** string

Always an empty string.

**cited\_text** string

The answer text of the current text block up to this citation. Unlike the Anthropic API, it is not text quoted from the source.

**[Text delta]**

**type** stringrequired

**Possible values:** `content_block_stop`

**index** integerrequired

**Possible values:** `>= 0`

Zero-based index of the content block.

**[Thinking delta]**

**type** stringrequired

**Possible values:** `message_delta`

**delta**

object

required

**stop\_reason** stringrequired

**Possible values:** `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `refusal`

The final reason generation stopped.

**stop\_sequence** stringnullablerequired

The matched stop sequence, or null when no stop sequence was matched.

**stop\_details**

object

nullable

Present when the model content safety review refuses the response (`stop_reason` is `refusal`). See the [Model Content Safety Guide](../guides/safety.md#handling-refusals).

**type** stringrequired

**Possible values:** `refusal`

**category** stringnullable

Always `null`.

**explanation** stringnullable

Names the blocked images when images in the request fail the review; otherwise `null`.

**title** string

DeepSeek extension. The conversation title, present only when the request enabled `title` and a title was generated.

**usage**

object

required

**input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens not served from the context cache. Total input tokens equal input\_tokens + cache\_read\_input\_tokens + cache\_creation\_input\_tokens.

**cache\_creation\_input\_tokens** integerrequired

**Possible values:** `0`

Always 0. Anthropic-style cache creation is not used; context caching is automatic.

**cache\_read\_input\_tokens** integerrequired

**Possible values:** `>= 0`

Input tokens served from the context cache.

**output\_tokens** integerrequired

**Possible values:** `>= 0`

Generated output tokens, including thinking tokens when thinking is enabled. In message\_delta this is the cumulative count, not an increment.

**output\_tokens\_details**

object

Breakdown of `output_tokens`. Present when thinking is enabled or `safety_check` is `high`.

**thinking\_tokens** integer

**Possible values:** `>= 0`

Thinking tokens, already included in `output_tokens`.

**safety\_tokens** integer

**Possible values:** `>= 0`

DeepSeek extension. Tokens of the safety review, already included in `output_tokens`. Present only when `safety_check` is `high`.

**service\_tier** stringrequired

**Possible values:** `standard`

**server\_tool\_use**

object

Server-side web search and fetch counts, separate from token usage. Present only when at least one of the counts is greater than zero; otherwise omitted. All fields are present when this object is returned. Read the final message's usage for non-streaming responses or the final message\_delta.usage for streaming responses. These counts are cumulative, not deltas. See [Server tool usage](../guides/anthropic_api.md#server-tool-usage).

**web\_search\_requests** integerrequired

**Possible values:** `>= 0`

Number of server-side web search attempts, including failed attempts and attempts exceeding `max_uses`.

**tool\_search** integerrequired

**Possible values:** `>= 0`

Number of successful server-side web searches that returned nonempty results. Failed attempts and empty results are not counted. This field can be used as a basis for billing.

**web\_fetch\_requests** integer

**Possible values:** `>= 0`

With the web tools. Number of fetch result blocks in the response, including errors. For display only.

**tool\_fetch** integer

**Possible values:** `>= 0`

With the web tools. Number of billed page fetches.

**tool\_image\_search** integer

**Possible values:** `>= 0`

With the web tools. Number of billed image searches.

**[Signature delta]**

**type** stringrequired

**Possible values:** `message_stop`

**[Tool input delta]**

**type** stringrequired

**Possible values:** `ping`

- ]

**[Citations delta]**

```shell
event: message_start
data: {"type":"message_start","message":{"id":"e6ef6a63-a078-4f53-a73b-38c8d1d46310","type":"message","role":"assistant","model":"deepseek-flash","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":12,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":0,"service_tier":"standard"}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type":"ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello!"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"input_tokens":12,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":3,"service_tier":"standard"}}

event: message_stop
data: {"type":"message_stop"}
```

Invalid request, for example an empty `messages` array or unpaired tool results. Errors use the Anthropic structure `{type: "error", error: {type, message}}`, where `error.type` follows the HTTP status: `invalid_request_error` (400, 422), `authentication_error` (401), `billing_error` (402), `permission_error` (403), `not_found_error` (404), `request_too_large` (413), `rate_limit_error` (429), `timeout_error` (408, 504), `overloaded_error` (503) and `api_error` (500 and others). See [Error Codes](../quick_start/error_codes.md) for the causes of each status.

**[application/json]**

- Schema
- Example

**[Schema]**

**Schema**

**type** stringrequired

**Possible values:** `error`

Always `error`.

**error**

object

required

**type** stringrequired

The error type, such as `invalid_request_error` or `rate_limit_error`.

**message** stringrequired

A description of the error.

**[Example]**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "messages: at least one message is required"
  }
}
```

Loading...
