---
layout: default
title: Terminology
nav_order: 2
---

# Terminology

## A

### Agent
Automation or AI-driven worker that executes tasks on Kawa data using configured tools, prompts, or triggers. Agents can read/write sheets, update views or reports, and participate in workflows. They run with assigned permissions and follow workspace policies.

**Used in:** [AI Integration](06_00_ai_integration.md) section.

---

## C

### Column
A field inside a Sheet that can represent row-level values or aggregated/metric values, depending on its definition. Columns are model attributes/metrics that inherit logic from source Indicators (DS) and Sheet transformations, and act as the canonical inputs for Fields. Columns may be raw (ingested from a data source) or computed (formula, lookup, mapping).

**Used in:** [Data Modeling](02_00_modeling.md) section.

### Control Panel
A configurable set of user-facing controls that manages both filters (applied to one or many Views/Sheets/Reports) and variables used to configure scenarios and referenced in formulas/metrics. It defines scope, default values, and propagation rules for governed self-service.a configurable set of user-facing controls that manages both filters (applied to one or many Views/Sheets/Reports) and variables used to configure scenarios and referenced in formulas/metrics. It defines scope, default values, and propagation rules for governed self-service.

**Used in:** [Control Panel](02_01_control_panel.md) section.

---

## D

### Data Source
A managed connection that supplies data to Kawa (database, SaaS, API, file, or internal provider). A Data Source defines connectivity, credentials, sync behavior, and schema discovery. It is the entry point of the modeling flow before transformation within Sheets.

**Used in:** [Data Integration](01_00_data_integration.md) section.

---

## F

### Field
The contextual use of a Column within a View, specifying role (axis, series, grouping, color, size, value) and aggregation behavior. Fields control how data is rendered and summarized, without changing the underlying column definition.
**Used in:** [Grid views](04_01_grid_views.md) section.

### Filter
A rule that restricts the dataset evaluated or displayed by a View, Sheet, or Report. Filters define conditions, scope (local vs global), and interaction with Control Panels; they do not alter persisted data, only the active query context.

**Used in:** [Filtering data](04_04_filtering.md) section.

---

## I

### Indicator
Indicator — a business metric defined at the Data Source level, used as the single source of truth for metrics that Sheets reuse.

**Used in:** [Data Integration](01_00_data_integration.md) section.

---

## K

### Knowledge
Curated reference content—definitions, guidelines, and organizational context—available to users and Agents during analysis and automation. Knowledge improves consistency of terms and decisions across a Workspace.

**Used in:** 

---

## P

### Python Tool
The managed Python execution capability in Kawa for custom logic. Python Tool runs scripts with controlled access to Kawa data and services, supports dependency management, and can be invoked by Workflows or Agents.

**Used in:** [Python Tools](09_02_python_tools.md) section.

---

## R

### Reports 
Published collections of Views arranged with layout, shared Filters, and optional Control Panels for interactivity. Reports define audience, permissions, and refresh behavior, serving as the primary distribution surface for indicators and analyses.

**Used in:** [Reports](05_01_reports.md) section.

---

## S 

### Sheet
A tabular model within Kawa that prepares data for analysis. Sheets join sources, apply formulas, lookups, and mappings, and establish validated Columns that downstream Views and Indicators reuse. Sheets are the governed transformation layer of the workspace.

**Used in:** [Data Modeling](02_00_modeling.md) section.

---

## T

### Team
A managed group of users with shared roles, permissions, and ownership within a Workspace. Teams control access to data sources, sheets, views, and reports, and can be targeted by workflows and sharing policies.

**Used in:** [Sharing and permissions](08_01_permissions.md) section.

---

## V

### View
A saved representation of data—grid, chart, or pivot—configured with Fields, Filters, and formatting. Views govern how data is queried and displayed and act as reusable building blocks inside Reports and applications.

**Used in:** [Data Modeling](02_00_modeling.md) section.

---

## W

### Workspace
The top-level environment that contains data sources, sheets, views, reports, automations, knowledge, and teams. A workspace defines governance (roles, policies), resources, and collaboration boundaries for a project or organization.

**Used in:** [Sharing and permissions](08_01_permissions.md) section.

---

## Key “vs” comparisons

### Column vs Field vs Indicator

- Column — a defined field in a Sheet (the model’s data element), sourced or derived (dimension, measure, calculated, or metadata), used for querying, filtering, grouping, and optional aggregation.
- Field — the visual role of a column in a View (how it’s presented/aggregated).
- Indicator — metric at the Data Source level (source of truth for business metrics).

**Relationship**: Indicators (Data Source) → inform Columns (Sheet) → become Fields (View).

### View vs Reports

- View — one saved visualization (grid/chart/pivot).
- Reports — a collection of views with shared filters and layout.

### Data Source vs Sheet

- Data Source — data imported or synchronized from underlying systems (files, databases, APIs, SaaS еtс).
- Sheet — Sheet — the data model built on top of one or more data sources, where you define metrics for downstream use.

### Filter vs Control Panel

- Filter — a rule that restricts the dataset for a View/Sheet/Report; sets conditions and scope (local/global) and affects the query context without changing stored data.
- Control Panel — a configurable set of user controls that manages filters and variables across Views/Sheets/Reports; defines scope, default values, and propagation, and exposes variables reusable in formulas/metrics.