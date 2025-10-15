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

> You can read more about this in the [The Workflows section](07_00_workflows.md).

- Set it up in **Home** → **Workflows** (click **+ Workflow**).

![Release](./readme-assets/release(1.34)1.png)

- Trigger types (**WHEN**): Daily / Intraday / Weekly / Monthly / Manual only + Timezone and Only on business days.

![Release](./readme-assets/release(1.34)2.png)

- Actions (**THEN**): Transform data (Sheets), Run python script (from the library), Send email, AI prompt.

![Release](./readme-assets/release(1.34)3.png)

- **Bindings** link fields from the current step to outputs from previous steps, passing data between actions in a workflow.

![Release](./readme-assets/release(1.34)4.png)

- **Save & Update**: Click **Create workflow** to save a new workflow; after any edits, click **Update workflow**.

- **Run & monitor**: open **Run history** (top‑right) → Run for ad‑hoc execution; review Start / End / Status / Error with counters (Total / Success / Failed) and date filters.

![Release](./readme-assets/release(1.34)5.png)

**Workflows** make it easier than ever to turn your data into action—automate routine tasks, deliver consistent email/AI outputs, and stay safe with built‑in guardrails and run history.

### 1.2 Doc — a free-length document page that combines text and interactive widgets.

> You can read more about this in the [The Reports section](05_01_reports.md).

- Set it up in **Home** → **+ Report** → **Doc** (next to Dashboard and Slides).
- Quick **block** insert via + or /: Text, H1–H3, Bulleted/Numbered list, Checklist, Сode, Image, Add widget.

![Release](./readme-assets/release(1.34)6.png)

- **Block handle** (six dots) with context menu: Convert to, Move up/Move down, Delete.

![Release](./readme-assets/release(1.34)7.png)

- **Add widget** in a Doc: choose a Sheet → Existing or New widget (chart, grid, pivot).

![Release](./readme-assets/release(1.34)8.png)

- **Filters & exploration**: work the same as in dashboards (Control panel, Exploration mode).
- **Widget actions** (Refresh, Summary, Edit, Full screen, Rename, Disable/Enable all filters, Duplicate, Synchronize, Go to sheet, Delete) — identical to Dashboard.

**Doc** turns insights into stories—write your narrative, drop in live widgets, and share a single scrollable page that stays in sync with your data.