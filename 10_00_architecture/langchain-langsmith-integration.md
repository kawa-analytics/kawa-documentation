---
title: LangChain / LangSmith integration
parent: Architecture
nav_order: 39
---

# LangChain / LangSmith integration

KAWA's AI features, and Riyu in particular, can run entirely on the LLM stack you already operate. Riyu sends its model calls to a **LangChain gateway** that you configure; the gateway routes them to your model provider and reports every call to **LangSmith**. You choose the models, you keep the traces, and nothing leaves your network unless you decide it should.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/langchain-langsmith-integration.png" alt=""><figcaption></figcaption></figure></div>

_Riyu and the KAWA workspace send their LLM calls to the LangChain gateway, which routes them to your provider and traces them in LangSmith._

## 1. Overview

| Component                   | Role                                                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Riyu and the KAWA workspace | Send every LLM call to the gateway as a standard chat completion request. No vendor SDK, no vendor key inside KAWA.                                                                                |
| LangChain gateway           | A single container shipped with Riyu. It exposes an OpenAI-compatible endpoint, maps three model aliases (`small`, `medium`, `large`) to the models you pick, and applies your policies.           |
| Your model provider         | Any provider LangChain supports: AWS Bedrock, Azure OpenAI, Google Vertex AI, OpenAI, Anthropic, or open models served on-premise.                                                                 |
| LangSmith                   | Receives a trace of every call: prompt, tool calls, tokens, cost and latency, tagged with the KAWA user and project. Runs in the LangSmith cloud or self-hosted inside your network.               |

## 2. Configuration

Three steps, all in the Riyu environment file. No code, no rebuild.

### 2.1 Point Riyu at the gateway

```
SMALL_MODEL=langchain/small
MEDIUM_MODEL=langchain/medium
LARGE_MODEL=langchain/large
LANGCHAIN_GATEWAY_URL=http://langchain-gateway:8000/v1
LANGCHAIN_GATEWAY_KEY=<shared secret between Riyu and the gateway>
```

Riyu uses `small` for quick tasks, `medium` for routine work and `large` for planning and building. The three aliases can point to the same model.

### 2.2 Choose your models

The gateway resolves each alias with a LangChain provider string and the credentials you give it. Only the gateway container holds those credentials.

```
MODEL_SMALL=bedrock_converse:<model id>
MODEL_MEDIUM=bedrock_converse:<model id>
MODEL_LARGE=bedrock_converse:<model id>
```

| Provider                 | Provider string             | Credentials                                          |
| ------------------------ | --------------------------- | ---------------------------------------------------- |
| AWS Bedrock              | `bedrock_converse:<model>`  | Standard `AWS_*` variables or an instance role       |
| Azure OpenAI             | `azure_openai:<deployment>` | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`      |
| Google Vertex AI         | `google_vertexai:<model>`   | `GOOGLE_APPLICATION_CREDENTIALS` (service account)   |
| On-premise / open models | `ollama:<model>`            | None, the gateway talks to your local model server   |

Mixing providers is fine: a small on-premise model for `small` and a hosted frontier model for `large` is a common setup.

### 2.3 Connect LangSmith

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your LangSmith key>
LANGSMITH_PROJECT=riyu-production
LANGSMITH_ENDPOINT=https://langsmith.your-company.com   # self-hosted LangSmith only
```

Restart Riyu. From the first conversation, traces appear in the LangSmith project.

## 3. What you get in LangSmith

* Every agent turn as a trace: the prompt, each tool call, tokens, cost and latency.
* Filters by KAWA user, project, autopilot and model alias. The gateway attaches them as metadata on every trace.
* Datasets and evaluations: replay real Riyu conversations against a candidate model before you switch to it.
* Feedback attached to runs, so a thumbs-down in Riyu lands next to the trace that caused it.
* Data masking with `LANGSMITH_HIDE_INPUTS` and `LANGSMITH_HIDE_OUTPUTS` for regulated content.

## 4. Governance and security

* **Credentials stay in one place.** Riyu never sees a provider key; only the gateway does.
* **One control point.** Model allow-list, PII masking, rate limits and cost caps are gateway policies, applied to every call from every user.
* **Switching providers is a configuration change.** Edit the provider strings in step 2.2 and restart. No change on the Riyu side.
* **Self-hosted LangSmith** keeps prompts and traces inside your perimeter. Combined with an on-premise model, no data leaves your network.

## 5. Frequently asked questions

**Do we need LangSmith?** No. Set `LANGSMITH_TRACING=false` and the gateway runs without tracing. LangSmith can be enabled later without any other change.

**Can we use our existing LangSmith project?** Yes. Set `LANGSMITH_PROJECT` to its name and the Riyu traces sit next to your other applications.

**Which models does Riyu need?** Riyu works best with a current frontier model behind `large`. Tool calling and streaming are required, which every provider in the table above supports.

**What about the AI features inside the KAWA workspace?** Formula assist, chart generation and the data chat use KAWA's own LLM configuration, which can be pointed at the same gateway so all AI traffic shares one policy and one LangSmith project.
