---
layout: default
title: Terminology
nav_order: 2
---

# Terminology

## A

### Agent
A workspace-wide AI assistant available in AI chats. Each agent is configured with instructions, connected knowledge sources (including unstructured data), a set of commands, and defined capabilities to help with tasks and queries. Every workspace includes a default agent (Paul) that can be edited but not removed; users with the Edit Agent flag can create, update, or remove other agents.

**Used in:** [AI Integration](06_00_ai_integration.md) section.

---

## C

### Column
An individual field/attribute in a Sheet that defines the sheet’s data structure. Columns can be dimensions, measures, calculated fields, or metadata fields. They may come directly from Data Sources or be derived (formulas, mappings, Python). Columns determine how the model can be queried, grouped, and visualized; their values can be shown as-is or further aggregated/formatted for analysis.

**Used in:** [Data Modeling](02_00_modeling.md) section.

### Control Panel
A configurable set of user-facing controls that manages both filters (applied to one or many Views/Sheets/Reports) and variables used to configure scenarios and referenced in formulas/metrics. It defines scope, default values, and propagation rules for governed self-service.a configurable set of user-facing controls that manages both filters (applied to one or many Views/Sheets/Reports) and variables used to configure scenarios and referenced in formulas/metrics. It defines scope, default values, and propagation rules for governed self-service.

**Used in:** [Control Panel](02_01_control_panel.md) section.

---

## D

### Data Source
A single data table in KAWA. It contains Indicators (columns) with defined types (e.g., date, datetime, text, boolean, integer, decimal; lists of texts/numbers are supported) and must have a primary key (single or composite) that uniquely identifies each row.

**Used in:** [Data Integration](01_00_data_integration.md) section.

---

## F

### Field
The contextual use of a Column within a View, specifying role (axis, series, grouping, color, size, value) and aggregation behavior. Fields control how data is rendered and summarized, without changing the underlying column definition.
**Used in:** [Grid views](04_01_grid_views.md) section.

### Filter
A condition that limits the records returned and shown by KAWA when a View, Sheet, or Report is evaluated. A filter specifies fields, operators, and values; it can be saved with a view, defined on a sheet, or applied report-wide. Filters change what is queried and displayed; they do not modify stored data.

**Used in:** [Filtering data](04_04_filtering.md) section.

---

## I

### Indicator
A Data Source column (one field of the source table). Indicators have a defined type (e.g., date, datetime, text, boolean, integer, decimal; lists are also supported) and may be part of the primary key (single or composite) that uniquely identifies rows. Indicators are listed in the Data Source overview and are the inputs used when building Sheets.

**Used in:** [Data Integration](01_00_data_integration.md) section.

---

## K

### Knowledge
A workspace section for connecting and integrating unstructured data (documents, files) into KAWA to support data-driven work. This feature requires a connection to OCR (Optical Character Recognition) and to a completion API.

**Used in:** 

---

## P

### Python Tool
A Python function registered in KAWA with the @kawa_tool decorator (from kywy.client.kawa_decorators). Tools run on KAWA’s Python runtimes configured at the workspace level. You can add tools in two ways:
1. KAWA File Store — write/edit the script directly in the GUI;
2. Connected VCS (Git over SSH) — KAWA clones/pulls your repo; each repo includes requirements.txt and a kawa-toolkit.yaml that groups tools into toolkits.
When a tool is added from VCS, it is not editable in the GUI (update via commits). Tools declare inputs/outputs in the decorator, appear in the Tools section, and require the appropriate workspace permissions and a healthy Python setup.

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
- Sheet — the data model built on top of one or more data sources, where you define metrics for downstream use.

### Filter vs Control Panel

- Filter — a rule that restricts the dataset for a View/Sheet/Report; sets conditions and scope (local/global) and affects the query context without changing stored data.
- Control Panel — a configurable set of user controls that manages filters and variables across Views/Sheets/Reports; defines scope, default values, and propagation, and exposes variables reusable in formulas/metrics.