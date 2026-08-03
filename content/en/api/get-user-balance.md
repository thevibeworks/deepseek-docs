---
title: "Get User Balance"
description: "Get user current balance"
source: https://api-docs.deepseek.com/api/get-user-balance
fetched: 2026-08-02
---

# Get User Balance

```
GET /user/balance
```

Get user current balance

## Responses

- 200

OK, returns user balance info.

**[application/json]**

- Schema
- Example (from schema)
- Example

**[Schema]**

**Schema**

**is\_available** boolean

Whether the user's balance is sufficient for API calls.

**balance\_infosobject[]**

- Array [

**currency** string

**Possible values:** [`CNY`, `USD`]

The currency of the balance.

**total\_balance** string

The total available balance, including the granted balance and the topped-up balance.

**granted\_balance** string

The total not expired granted balance.

**topped\_up\_balance** string

The total topped-up balance.

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
