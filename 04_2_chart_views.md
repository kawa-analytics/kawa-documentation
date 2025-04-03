---
layout: default
title: Chart Views
parent: Visualization
nav_order: 7
---

Chart views
---

Chart views let you build powerful visualizations of your data.
Many different types of charts are available and each one support a wide range of configuration parameters.

* TOC
{:toc}

In order to create a new Chart View, click on the plus button at the top left of your sheet, and pick: Chart.

# 1 Configure  your Chart

Configuring your chart is made through the Configure chart menu, accessible from the top right.

![Chart config](./readme-assets/chart_view_config1.png)

*There are three main sections in the chart configuration panel: Data, Design and Settings.*

You can pick your chart type at the top of the configuration panel.

## 1.1 Configure a bar chart

In the data section, pick the Series and the Groupings.
A bar chart can have one or two levels of grouping and does not have any limit in the number of series.

> It is strongly recommended to have only one series when two levels of grouping are present.


### a. Bar chart with one level of grouping and one or more series

In a bar chart, the first level of grouping will always be the X-Axis.

When configuring a chart with multiple series and one grouping, you can decide to stack the series or show them separately. 

The stacking option is found in the design section, in the upper horizontal tab.

![Chart config](./readme-assets/chart_view_bar_chart_1.png)

![Chart config](./readme-assets/chart_view_bar_chart_2.png)

*Bar chart showing the profit and sales per sub-category, with and without Stacking*


### b. Bar chart with two levels of grouping and one series

With two levels of grouping, the first level will be the X-Axis and the second level will be reflected as the various portions of each bar.

![Chart config](./readme-assets/chart_view_bar_chart_3.png)

*In the above example, you can see that the first level of grouping (Months) is shown on the X-Axis, while the second level of grouping is reflected on each bar (One color per year)*


### c. Specific settings for the bar charts

In the design section, you have several options to customize your bar charts:

- Formatting of each series
- Setting colors to each series or each point for the second level of grouping
- Defining gaps between bars
- Show the totals on top of each bar
- Make the bar chart horizontal (Only works for one level of grouping)


## 1.2 Configure a line chart

Line charts are similar to Bar charts, but are generally preferred to plot trends or evolutions of metrics.

In the data section, pick the Series and the Groupings.
A line chart can have one or two levels of grouping and does not have any limit in the number of series.

> It is strongly recommended to have only one series when two levels of grouping are present, otherwise the chart will be difficult to read.



### a. Line chart with one level of grouping and one or more series

