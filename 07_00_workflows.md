---
layout: default
title: Workflows
nav_order: 25
---

# Workflows

**Workflows** is KAWA’s builder for multi-step processes. Actions can be started on a schedule or manually, and steps run in sequence: data processing, running Python scripts, sending emails, and calling AI prompts.

* TOC
{:toc}

## 1. First workflow: Create

To create a new workflow, go to the **Workflows** section and click on **+ Workflow**.

![Workflows](./readme-assets/workflows1.png) 

## 2. Set trigger

KAWA Workflows support two trigger types. Pick one in **WHEN** → Select a trigger.

### 2.1 At a scheduled time

Use this when the workflow must run automatically.

- Choose **At a scheduled time**.
- Configure:

  - **Daily** / **Intraday** / **Weekly** / **Monthly**.
  - Run time:

>Daily — Run at → pick an exact time (e.g., 09:00).
>Intraday — Run every N [seconds/minutes/hours]; optionally turn on Set custom time period.
>Weekly — Run on (choose weekdays) at (time).
>Monthly — Run every month on (day of month) at (time).

  - **Timezone**.
  - **Only on business days** (optional).

- The header shows the summary (e.g., Runs daily at 09:00).

![Workflows](./readme-assets/workflows2_1.png)

### 2.2 Manual run

Use this when the workflow is started on demand by a user.

- Choose **Manual run**. 
- (Optional) Click **+ Add input** to define parameters that the user must enter each time they start the run: **Text**, **Number**, **Date**, **Date Time**, **Boolean**.
- These inputs are available to later steps via bindings:
    - In Email / AI prompt editors: click **+** → Use data from → Choose data, then choose the input.
    - In Run python script, Parameters:  click **+** → Use data from → Choose data, then choose the input.

![Workflows](./readme-assets/workflows2_2.png)

## 3. Add action

Click **Add action** — the Actions panel opens; select the needed action.

![Workflows](./readme-assets/workflows3.png)

### 3.1 Step 1: Transform data

- Choose a **Sheet** from the list.

![Workflows](./readme-assets/workflows4.png)

- If needed, open Enrich data and use the quick transform icons.

![Workflows](./readme-assets/workflows5.png)

- In the **Behavior** block, set:

  - If no rows are found → Interrupt workflow / Continue without a result.
  - If more than 50 rows are found → Interrupt workflow / Continue  without a result.
  - Max number of rows → a number (e.g., 50).

### 3.2 Step 2: Run python script

- In **Select python tool from the library**, choose a tool.

![Workflows](./readme-assets/workflows6.png)

- In **Match tool inputs** (required entries), bind inputs to outputs from previous steps:
  - **df** → select **1. Transform data** or other prior action.
  - **text** → bind to a source.

> If a required input is empty or mis‑bound you’ll see **Invalid task bindinqs**.

![Workflows](./readme-assets/workflows7.png)

- **Parameters** (optional/named options) → they can also be bound to outputs from previous steps.

> If a parametrs is empty you’ll see **Invalid parameter bind**.

**Behavior** — the same row-based guards as in Transform data appear at the bottom.

### 3.3 Step 3: Send email

**Recipients**, **Subject**, and **Body** can be entered manually, or use the **+** on the right to insert values from previous steps (e.g., a sales total or a generated table).
>If a required fields is empty you’ll see **Invalid parameter bind**.

![Workflows](./readme-assets/workflows8.png)

### 3.4 Step 4: AI prompt

- Enter the prompt text. Use the **+** button to insert variables/fragments from previous steps (transformation results, script outputs, etc.).

![Workflows](./readme-assets/workflows9.png)

- Use the prompt for summarization, recommendations, and generating explanations.

## 4. Save

Сlick **Create workflow**.

![Workflows](./readme-assets/workflows10.png)

## 5. Update workflow

When you open an existing workflow from **Home** → **Workflows**, the editor shows the current **WHEN** (schedule) and **THEN** steps. The **Create workflow** button is replaced with **Update workflow** (bottom-right). Update workflow saves changes to an existing workflow (schedule, steps, bindings, Behavior). After saving, both scheduled and manual runs use the latest version.

## 6. Manual run & history

Use manual runs to test or trigger a workflow on demand. A manual run does not change the schedule.

### 6.1 Run from the workflow editor

- Click **Run history** (top-right).
- In the modal, press **Run** to start immediately.
- The table shows Start, End, Status, and Error for each attempt. Use the date filters and counters (Total / Success / Failed) to review past runs.

![Workflows](./readme-assets/workflows11.png)

![Workflows](./readme-assets/workflows12.png)

### 6.2 Run from Home → Workflows

- Open **Home** → **Workflows**.
- In the row of a workflow, open the three-dot menu → **Run**.
- The current **Status** appears in the list; open the workflow and Run history for details.

**Status** shows the last result: **Success, Failed, Running, Stopped**.

## 7. Reorder / Delete steps

- **Reorder**: drag & drop steps in THEN. If you move a step above its data source, dependent steps show Invalid task ref; open them and re-bind fields via +.
- **Delete**: trash icon on a step. Steps referencing a deleted step also show Invalid task ref — fix or remove those bindings. Deletion can’t be undone.

