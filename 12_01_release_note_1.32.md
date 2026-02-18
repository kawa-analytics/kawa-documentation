---
title: Release note - KAWA 1.32
parent: Release Notes
nav_order: 41
---

# Release note 1.32

* TOC {:toc}

## 1. New Features

### 1.1 Cross Filters — on dashboards, filter multiple widgets at once with a single selection

* Set it up in the **Config panel**.

![Release](.gitbook/assets/release\(1.32\)1.png)

* Active filters show as chips at the top.

![Release](.gitbook/assets/release\(1.32\)2.png)

* Each widget has a filter status icon that lists active filters (cross + dashboard + control panel) and displays whether they are enabled/disabled for this widget. ![Release](.gitbook/assets/release\(1.32\)4.png)

Benefits: fewer duplicate filters, faster analysis, shared context across widgets.

### 1.2 Widget in full screen mode in application and dashboard

All type of widgets ( charts , pivot and grid) will have an new icon full screen in dashboard and application.

![Release](.gitbook/assets/release\(1.32\)5.png)

### 1.3 The query cache on external DataSources

Query cache configuration (per data source). Turn caching on/off, set TTL in seconds, and define an optional daily UTC window when cache is bypassed. Existing Clear query cache action remains available. For complete documentation and setup details, please visit: [KAWA Query Cache](10_03_query_cache/) section.

### 1.4 Python scripts: File upload parameters

Add a file-upload field to a script by setting 'fileExtensions'. Users can upload only the allowed formats, and Apply stays disabled until all required files are uploaded.

![Release](.gitbook/assets/release\(1.32\)6.png)

### 1.5 Run Python tool for scripts without inputs/outputs

Triggers a script with no inputs/outputs (scriptType: "RUNNABLE"). Pick the script in the control settings (FE stores the scriptId; no Python private join/mapping needed). On click the script runs and the view auto-refreshes when it’s done.

![Release](.gitbook/assets/release\(1.32\)7.png)

### 1.6 Create input table

Create an editable data source in two ways:

![Release](.gitbook/assets/release\(1.32\)8.png)

Start from scratch — same flow as before, with a richer creation modal for custom columns.

![Release](.gitbook/assets/release\(1.32\)9.png)

Quick upload — upload a CSV and start editing right away (uses the existing CSV upload component).

## 2. Improvements & Bugs fixes

### 2.1 Python

* Applications API: The extended application endpoint now returns the app’s current sheets alongside existing metadata. This lets clients fetch everything in one call.
* Further optimisation of Python server

### 2.2 Data edit

* Data constraints in datasource model
* Copy / PAste ranges of data

### 2.3 Pivot table & charts

* Improved pivot table functionality (Modify Pivot behaviour)
* Charting improvements
* Add stacked line chart
* Changed legend behaviour

### 2.4 Other

* Security mapping for Live connections. Map source-side row/column permissions to KAWA roles when the data source uses Live connection.
* UI updates (Dashbords, Applications, Control panel)
* Add filter null in CP filter
* Fix BUG in last date filter (on date time)
* Improved exploration mode in apps
* Improved all home pages grids
