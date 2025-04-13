---
layout: default
title: Data Modeling
nav_order: 4
---

Data Modeling - Sheets
---

In KAWA, sheets can be used in several ways.

The easiest way is to use them like an Excel Workbook, adding multiple views (Tabs) to explore and visualize your data: cf [The Visualization section](./03__visualization).


However, sheets are much more powerful than that and can be used to build and share your enterprise data models.

# 1. The structure of a Sheet

A sheet is composed of the following main elements:

- A main data source
- Several linked data sources (Optional)
- Some views, with at least a Grid view
- Some columns (similar to the columns of a table in a database)
- Some metadata

All these concepts will be explored in specific pages.

## 1.1 The main data source

The main data source of a Sheet (cf [Data Integration](./01__data_integration) for details about data sources) will dictate the sheet data granularity. In other words, it will define the primary keys of your sheet. 

For example, if you choose a position system as a main data source, your sheet will show data per asset and portfolio.

> The primary data source is set during sheet creation and cannot be modified afterward.


## 1.2 Linked data sources

You can add several linked data sources to an existing sheet. They will be used to enrich your sheet with data coming from various systems and data sets. Because main data source imposes its granularity, the linked data sources will not affect the number of row, but rather adding columns to existing ones. 

In a database vocabulary, the linked data sources will be joined using `LEFT JOIN` only.

> Working with a Star Schema for example, where you would have one central Transaction table and related dimension tables: you would create a sheet on the Transaction table and then join in the various dimension tables.

## 1.3 Views

A Sheet contains views that offer diverse perspectives on its data. cf the [The Visualization section](./03__visualization).

## 1.4 Columns

The columns of a sheet represent the individual fields or attributes that define the structure of its data. Each column corresponds to a specific type of information, such as:

- __Dimensions__ – descriptive fields like names, dates, or categories.

- __Measures__ – numeric values that can be aggregated, like sales or quantities.

- __Calculated Fields__ – custom columns derived from expressions or formulas based on other columns.

- __Metadata Fields__ – technical or structural data, such as IDs or timestamps.

Columns define what kind of data the model captures and how it can be queried, grouped, and visualized.

Columns can originate directly from the underlying data sources or be derived through formulas, mappings, Python scripts, and more. Their values can be displayed as-is, or further aggregated and formatted for analysis and visualization.


## 1.5 Metadata

In a sheet, metadata refers to the descriptive information that defines and contextualizes the structure and behavior of the underlying data model.

It includes details such as 
- Global description of the sheet (consumed by AI)
- Column names,
- Column descriptions, 
- Data types, 
- Relationships between data sources, 

It also captures how data should be aggregated, formatted.

This layer of information ensures consistency, enhances data discoverability, and enables more meaningful and efficient analysis across various views and visualizations.

