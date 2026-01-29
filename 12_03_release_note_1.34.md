---
layout: default
title: Release note - KAWA 1.34
parent: Release Notes
nav_order: 43
---

# Release note - KAWA 1.34

* TOC
{:toc}

## 1. New Features

### 1.1 Workflows — more triggers, actions, and control flow

> You can read more about this in the [The Workflows section](./07_00_workflows).

Workflows now support richer automation from end to end:

- **New trigger: On data refresh** — run a workflow automatically right after a selected data source refreshes (supports multiple sources with **OR** logic).

![Release](./readme-assets/release(1.34)_workflows1.png)

- **New actions** to build pipelines without leaving the editor

![Release](./readme-assets/release(1.34)_workflows2.png)

  - **Enrich data with AI** (generate output columns per row)
  - **Report** (select a report from the workspace and use it later in the workflow as an artifact)
  - **Build a chart** (from previous steps or any Sheet)
  - **Export to data source** (export a table result with export mode + access policy)
  - **Generate output** (produce a text result using variables from prior steps)

- **New logic blocks** for advanced orchestration

  - **If / Else** with multiple rules (**AND** logic), comparing values from prior steps (grid, aggregates, properties)
  - **Routing** to split one input table into multiple routes (R1/R2/R3…), each with its own slice and actions
  - **Interrupt workflow** to immediately stop execution (useful as an “emergency stop” inside branches/routes)

- **More ways to run workflows**: from the **Controls panel** (button → Run workflow) and from **AI Chat** as Agent commands (add workflows to an agent and run them directly from chat)

### 1.2 Create Multi-sheets — support Pivot tables and Charts across multiple sheets

Now user can create a **Multi-sheet** (a combined sheet) that consists of several child sheets. A Multi-sheet supports working with multiple primary data sources in one object.

![Release](./readme-assets/release(1.34)_multisheets1.png)

- Multi-sheet supports **Pivot Table** and **Chart** as the main modes (Grid Flat is disabled), so user can build visualizations using columns from different child sheets.

![Release](./readme-assets/release(1.34)_multisheets2.png)

- **Filters** show all Multi-sheet columns (from all child sheets).
- A **2-level hierarchy** was added to the column picker: **Data sources** → **Columns**, so sources don’t get mixed into one list and the setup is easier to understand.

![Release](./readme-assets/release(1.34)_multisheets3.png)

- For Multi-sheet, the “Join a new data source” option was removed.
- For Multi-sheet, AI Chat and Automations are disabled; the Model is still available, but read-only.
- Editing actions that don’t make sense for Multi-sheets were removed: Edit linked columns and mapping edit.

## 1.3 Views — cancel a computation 

Long-running computations can now be interrupted directly from the loading state using a **Cancel** action. A new backend command, InterruptComputation, stops the current computation and returns a **CANCELLED** status (with metadata and empty records).

![Release](./readme-assets/release(1.34)_cancel.png)

## 1.4 Reports — Read-only (View) mode

Reports now have a clearer **View** (read-only) mode designed for presenting and consuming content:

![Release](./readme-assets/release(1.34)_reports_view.png)

- A dedicated **View** mode toggle is available.
- When a user has **read-only** access, Reports open in View mode by default.
- The Control panel works in View mode: if at least one control exists, it is shown so viewers can apply filters without editing the report.
- Export to PDF is available in View mode.

## 2. Improvements & Bugs fixes

### 2.1 Data sources

- Changed data deletion permissions

### 2.2 Pivot table & charts

- Improved legend behaviour

### 2.3 Filters

- Improved Text filters: User can now paste a list of values copied from Excel into a text filter. KAWA converts line breaks into ; and automatically selects all pasted values (even if they are not currently in the list). The same behavior is supported in the **Control** panel.
- Improved date filter

### 2.4 Reports

- Improved AI widgets
- Visual polish and UI fixes

### 2.5 Python

- Scripts — built-in script library: Scripts can now be marked as built-in (builtIn: true) and surfaced as a dedicated “built-in” set in the Scripts list (with a filter). Built-in scripts are read-only for users: they can’t be deleted, renamed, edited (description), or shared — only Add to favorites is available.

### 2.6 Authentication

- Improved API key management

