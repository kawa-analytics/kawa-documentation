---
layout: default
title: Data Integration
nav_order: 3
---

Data Integration - Data Sources
---

There are several ways to connect KAWA with your data.
KAWA supports: Importing files, Connecting to external systems such as CRMs, databases, APIS etc, Linking to existing tables in the main warehouse, Importing unstructured data, Importing data from Python scripts.

# 1 Indicators

In KAWA, a Data Source corresponds to one data table. Each Data Source has a list of columns (referred to as `Indicators`). 

## 1.1 Indicator types

Each Indicator has a given type:

| Type | Example | Comment | 
|------|---------|---------|
| date    | 2025-06-25 | Dates do not have any timezone |
| date time | 2025-06-25 21:12:12 | Date times have a timezone and the precision depends on the settings of the KAWA instance. By default, date times are precise down to the millisecond. |
| text | 'Wayne' | |
| boolean | `true` or `false` | |
| integer | 1, 2, 0, -3 | |
| decimal | -0.3, 45.56 | |

KAWA also supports lists of texts and list of numbers.

## 1.2 Primary keys

Each Data Source includes at least one primary key, whose values uniquely identify every individual row within the dataset.

Let's take the example of a Data Source with some market data.

| Symbol  | Date       | Price    | 
|---------|------------|----------|
| WAYNE   | 2025-06-25 | 123.4    |
| WAYNE   | 2025-06-26 | 123.5    |
| WAYNE   | 2025-06-27 | 123.6    |
| WONKA   | 2025-06-25 | 234.5    |
| WONKA   | 2025-06-26 | 234.6    |
| WONKA   | 2025-06-27 | 234.7    |


It has three indicators:

- __Symbol:__ a text indicator, first primary key.
- __Date:__ a date indicator, second primary key.
- __Price:__ a decimal indicator 

Each row of the dataset is identified by the value of the symbol indicator and the date indicator. There cannot be any duplicate pairs (Symbol, Date).

## 1.3 Indicators in the KAWA GUI

In the KAWA GUI, the overview tab of each Data Source give information about its structure.

![Data](./readme-assets/data1.png)

On the right part, you can see all the indicators of the Data Source, with an icon representing the type, and a red key to represent whether or not an indicator is a primary key. Here, there are two primary keys: Symbol and Date.


# 2 Data profile and Data preparation





