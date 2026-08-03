# Release note - KAWA 1.35

## 1. New Features

### 1.1 New design for home pages

All **home pages** have been restyled — **Data Sources**, **Sheets**, **Workflows,** **Applications**, **Dashboards**, **Scripts**, **Agents**, and **Knowledge** now share a consistent, updated layout.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)1.png" alt=""><figcaption></figcaption></figure></div>

### 1.2 Workflows — Loop and Run workflow

In 1.35, Workflows gain two new capabilities — **Loop** for row-level iteration and **Run workflow** for composing workflows together.

> You can read more about this in the [Workflows section](../07_00_workflows/).

* **New logic block: Loop** — iterate over the rows of an input table, repeating a set of actions for each row.
* **New action: Run workflow** — run an existing workflow as a sub-workflow.

### 1.3 Workflows — new format for Run history

**Run history** is now rendered as an expandable tree. Loops, If / Else, Routing, and Sub-workflows appear as container rows with a count pill (e.g. **2 iterations**, **2 routes**, **Branch: Then**). Click the chevron to expand and inspect nested tasks.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)6.png" alt=""><figcaption></figcaption></figure></div>

### 1.4 Formula history

The formula editor now keeps a **Formula history**. Click the **clock icon** next to Input / Blockly / Ask AI to open a side panel listing saved formula versions with timestamps and authors. Click any version to load it back into the editor.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)2.png" alt=""><figcaption></figcaption></figure></div>

### 1.5 Sheets — Edit mode

Sheets based on an editable data source now support a dedicated **Edit mode**. Click **Edit data** in the action bar to open an edit session. Changes are no longer sent to the backend after each action — they are collected as pending edits and submitted in one pass when you click **Save**.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)3.png" alt=""><figcaption></figcaption></figure></div>

### 1.6 Sheets — Tab grouping

Views in a sheet can now be organized into groups. Each group is displayed as a colored tab with an icon in the view strip.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)4.png" alt=""><figcaption></figcaption></figure></div>

Open the group dropdown: pick a Style (color and icon), rename the group with an optional title, or Ungroup.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/release(1.35)5.png" alt=""><figcaption></figcaption></figure></div>

### 1.7 Sheets — Change data source

A new **Change data source** action in the **Model** tab lets you replace the primary data source of a sheet without losing its structure. KAWA guides you through a 4-step wizard: **Select source → Map columns → New columns → Review**.

<div data-with-frame="true"><figure><img src="../.gitbook/assets/change_data_source1.png" alt=""><figcaption></figcaption></figure></div>

* Columns are auto-matched by name and type. Key columns must remain mapped; non-key columns can be left unmapped.
* If the new source has extra columns, choose which ones to add to the sheet in the **New columns** step.
* Unmapped columns stay in the sheet but receive no data — they can be reconnected in a later replacement.
* Existing charts, pivot tables, filters, formulas, and lookup columns are preserved.

> You can read more about this in the [Change data source section](../02_00_modeling/change-data-source.md).

## 2. Improvements & Bugs fixes

### 2.1 Workflows

* Improved Stack datasets — the column mapping panel now offers three Column matching methods to auto-populate the mapped columns table: By column name, By column order, Auto-mapping.
* When a task's input comes from a previous task's output (not a data source), the editor now shows an info banner: "Preview data is a sample. Actual values will be computed when the workflow runs."

### 2.3 Pivot table & charts

* Pivot CSV export now offers two modes: Visible data (exports what's currently rendered, with formatting) and All data (raw) (full unformatted export from the backend).

### 2.2 ClickHouse

* Migrated from the JDBC driver to the native ClickHouse Java client. The new client reuses connection pools across requests and is backward compatible with ClickHouse LTS versions 24, 25, and 26.

## 3. Patch releases (1.35.x)

### Patch 1.35.1

* Splited datasources into Editable (created from scratch or via the Python client — full edit mode with add/remove rows and columns) and Patchable (backed by an external system — in-place cell patching only)
* Adapted the Print screen feature to the new backend, migrating its capabilities to Playwright on Java

### Patch 1.35.2

* Added a 3M (three-month) granularity option to date and date-time segmentation across the app
* Added the ability to duplicate a lookup (linked) column, like duplicating a formula, keeping the same target view, source field, aggregation, and join keys
* Added an "Edit data" toolbar to dashboard sheet widgets, letting users edit editable sheet views in place without full screen, with a buffered session that commits on Save or discards on Cancel
* Added a distinct icon for editable sheets wherever sheets are listed&#x20;
* Added a computed-columns count to each sheet in the home page catalog, updating automatically as computed columns are added or removed in the grid view
* Added an "Approval" input to the workflow form builder for User Input tasks, seeded with editable Approve/Reject options, that automatically generates an if/else branch per option after the task
* Added support for the new @kawa\_workflow\_tool decorator in Python workflow scripts, letting scripts declare input files, output files, output scalars, and named output data frames that downstream tasks can bind to, with an overview panel summarizing a tool's inputs and outputs
* Added view/edit for formula, lookup, and mapping columns in the Sheet model section
* Added a file trigger variable to workflows, so running a workflow can prompt the user to upload a file that is passed to the run
* Added a "Preview workflow" button to the sub-process task, opening a read-only preview of the selected sub-workflow
* Added multi-output support to Python workflow scripts, letting a script produce several named output data frames that downstream tasks can each select and bind to individually
* Added a "Left Anti Join" type to the workflow Join task, returning rows from Dataset A with no match in Dataset B
* Added a "Feed type" section to the data source overview showing the current loading mode, letting users switch between Incremental and Reset before insert with an inline warning about the impact, without needing a separate toolbar action
* Added editable multi-line descriptions to formula, lookup, and mapping columns, accessible from an info icon in their editors
* Added a per-series Bar / Line type toggle to grid-based charts, so a single chart can mix bar and line series
* Added support for integer and date columns as mapping keys, so mapping columns can key off numeric and date values in addition to text
* Added auto-matching of join columns by name, pre-selecting columns that exist on both sides of the join
* Added the ability to share entities with individual users, not just teams, via a single combined picker in the Share dialog with a Users / Teams toggle and a Viewer/Editor access level per user or team
* Reworked the workspace permissions UI with clearer role names (Explorer / Admin / Builder), a role field on the User Profile tab, a merged "Share and Write" group, and a highlighted "danger zone" for admin-level permissions
* Updated the workflow header to a breadcrumb-style header matching other entity pages (with inline rename, favourite star, share, and Workflow / Run history tabs), and improved the creation flow to prompt for a name and description
* Fixed formula creation in grid view so users without formula edit permission can create a new formula, instead of being blocked by a permission check that was mistakenly applied in create mode
* Fixed workflow updates to share the layouts backing COMPUTE/CHART tasks, so adding or rebuilding a task no longer leaves those layouts private and breaks workspace mounts for non-admin members
* Fixed workflow filters so an invalid or missing variable binding is surfaced and blocks saving, instead of failing silently until deploy, with the collapsed filter card showing the binding's real name and turning red when broken

