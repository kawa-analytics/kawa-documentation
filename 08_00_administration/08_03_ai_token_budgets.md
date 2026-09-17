# AI token budgets

An **AI token budget** caps how many AI tokens a user can consume in [Riyu](../riyu-ai-co-builder.md), per day and per month. It is set by a KAWA administrator on the user's account, and Riyu checks it before every piece of AI work it starts for that user.

> **Terminology:** In this document, "principal" refers to a KAWA user account. The terms are used interchangeably.

> **Important:** Every account starts with a budget of **zero** — no AI tokens at all — and there is no "unlimited" setting. After upgrading to 1.36.3, grant a budget to every user who should keep using Riyu.

## 1. How a budget works

A budget is two token counts stored on the principal:

| Window    | Meaning                                         | Resets                                       |
| --------- | ----------------------------------------------- | -------------------------------------------- |
| `daily`   | Tokens the user may consume in one calendar day | Every day at 00:00 UTC                       |
| `monthly` | Tokens the user may consume in one calendar month | On the 1st of each month at 00:00 UTC      |

* **Both windows always apply.** A user is blocked as soon as either one is used up, so both must be greater than zero for the user to work. A budget of `500000` daily and `0` monthly blocks the user.
* **What counts** — input, output and reasoning tokens. Prompt-cache traffic is tracked but does not count towards the budget.
* **What is covered** — everything Riyu runs on the user's behalf: chat, autopilot runs (counted against the user who created the autopilot), and agent-to-agent (A2A) calls made with the user's credentials.
* **When it is checked** — at the start of each chat turn, autopilot run or A2A call. Work already in progress is never cut off, so a user can finish slightly above the cap; the next start is then refused.
* **Who can set it** — KAWA administrators only. Users cannot change their own budget, and an account cannot be created with one: every new account starts at zero, whatever the creation request says.

## 2. Setting a budget

Budgets are set with the `ReplaceAiTokenBudget` command. It replaces the whole budget at once: always send both windows.

| Parameter     | Type    | Description                                                        |
| ------------- | ------- | ------------------------------------------------------------------ |
| `principalId` | string  | Id of the user — see [List users](../http-api-reference.md#id-3.1-list-users) |
| `daily`       | integer | Tokens per calendar day. Cannot be negative; omitted means `0`.    |
| `monthly`     | integer | Tokens per calendar month. Cannot be negative; omitted means `0`.  |

The command must be run by an administrator (with an administrator's API key). Anyone else is refused and the budget is left untouched. A value that is not a number is rejected — it is never read as "no limit".

### 2.1 With the HTTP API

```bash
curl -X POST https://your-instance.kawa.ai/commands/secured/run \
  -H "x-kawa-api-key: kawa_abc123xyz" \
  -H "x-kawa-workspace-id: ws_01" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ReplaceAiTokenBudget",
    "parameters": {
      "principalId": "p_01",
      "daily": 500000,
      "monthly": 10000000
    }
  }'
```

The response is the updated user, including its new `aiTokenBudget`.

### 2.2 With the Python SDK

```python
from kywy.client.kawa_client import KawaClient as K

kawa = K.load_client_from_environment()   # an administrator's API key

kawa.commands.run_command('ReplaceAiTokenBudget', {
    'principalId': kawa.commands.get_principal_entity_id('jane@acme.com'),
    'daily': 500_000,
    'monthly': 10_000_000,
})
```

To grant the same budget to several users, loop over their emails:

```python
for email in ['jane@acme.com', 'omar@acme.com', 'li@acme.com']:
    kawa.commands.run_command('ReplaceAiTokenBudget', {
        'principalId': kawa.commands.get_principal_entity_id(email),
        'daily': 500_000,
        'monthly': 10_000_000,
    })
```

### 2.3 Removing a budget

Set both windows to `0`. The user can no longer start AI work in Riyu; work already in progress finishes.

## 3. Checking a budget

The budget is part of the user record, under `aiTokenBudget`:

```json
"aiTokenBudget": { "daily": 500000, "monthly": 10000000 }
```

* An administrator reads it on any user with `GET /backoffice/principals/{id}`.
* A user reads their own with `GET /authentication/current-user`.

## 4. What users see

In Riyu, the user menu shows a **Usage** panel with the tokens consumed **Today** and **This month**, each against its cap and with the time of the next reset.

When a budget is used up, Riyu refuses the request before it reaches the AI and explains why, in the chat, in the autopilot's run history, or in the A2A error:

* `Your daily AI token budget is exhausted: 512,340 of 500,000 tokens used. It resets at 2026-09-18T00:00:00Z.`
* `No AI token budget is configured for your account — AI features are disabled until an administrator grants one.`

A chat request refused this way returns HTTP `429` with the error code `AI_TOKEN_BUDGET_EXCEEDED`, along with the consumption, the cap and the reset time of both windows.

## 5. Good to know

* **A change takes effect within a minute** — Riyu keeps each user's budget for up to 60 seconds before reading it again.
* **Consumption is kept per user, across workspaces** — a user has one budget for all the work they do in Riyu.
* **If Riyu cannot reach KAWA** to read a budget, it lets the work start rather than blocking everyone during an outage.
* **Choosing values** — start from observed consumption: the Usage panel shows what a user actually consumed today and this month. A monthly cap lower than the daily one simply means the monthly cap is reached first.
