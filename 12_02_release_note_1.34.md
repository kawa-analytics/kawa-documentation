---
layout: default
title: Release note - KAWA 1.34
parent: Release Notes
nav_order: 
---

# Release note - KAWA 1.34

* TOC
{:toc}

## 1. New Features

### 1.1 Workflows — design, schedule, and run multi‑step automations

- Set it up in **Home** → **Workflows** (click **+ Workflow**).

![Release](./readme-assets/release(1.34)1.png)

- Trigger types (**WHEN**): Daily / Intraday / Weekly / Monthly / Manual only + Timezone and Only on business days.

![Release](./readme-assets/release(1.34)2.png)

- Actions (**THEN**): Transform data (Sheets), Run python script (from the library), Send email, AI prompt.

![Release](./readme-assets/release(1.34)3.png)

- **Bindings** link fields from the current step to outputs from previous steps, passing data between actions in a workflow.

![Release](./readme-assets/release(1.34)4.png)

- **Run & monitor**: open **Run history** (top‑right) → Run for ad‑hoc execution; review Start / End / Status / Error with counters (Total / Success / Failed) and date filters.

![Release](./readme-assets/release(1.34)5.png)