---
title: "查询余额"
description: "查询账号余额"
source: https://api-docs.deepseek.com/zh-cn/api/get-user-balance
fetched: 2026-08-02
---

# 查询余额

```
GET /user/balance
```

查询账号余额

## Responses

- 200

OK, 返回用户余额详情

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**is\_available** boolean

当前账户是否有余额可供 API 调用

**balance\_infosobject[]**

- Array [

**currency** string

**Possible values:** [`CNY`, `USD`]

货币，人民币或美元

**total\_balance** string

总的可用余额，包括赠金和充值余额

**granted\_balance** string

未过期的赠金余额

**topped\_up\_balance** string

充值余额

- ]

**[Example (from schema)]**

```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

**[Example]**

```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

Loading...
