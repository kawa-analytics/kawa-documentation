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


__The settings tab:__ Contains global settings that apply for most types of charts. They let you control legend, behavior of axis, display properties and zoom.

The number of labels and label rotation work together. If you want to add more labels, you might need to rotate them by 45 or 90 degrees (vertical).


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

![Chart config](./readme-assets/chart_view_bar_chart_4.png)

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

In a bar chart, the first level of grouping will always be the X-Axis.

![Chart config](./readme-assets/chart_view_line_chart1.png)

*Simple line chart showing the evolution of profit per day*

When plotting multiple series for one grouping, you can decide whether to plot all series on the same axis or on diverse axis. If you choose the split chart option, you can have one chart per axis.

![Chart config](./readme-assets/chart_view_line_chart2.png)

*Plotting both Quantity (Ranges from -2 to 26 on a given date) and the Profit (Ranges from -200K to 3M on a given date) on two different axis.*


### b. Line chart with two levels of grouping and one series

Adding a second level of grouping on top of a temporal dimension is useful to see the breakdown of some indicator per another dimension.

![Chart config](./readme-assets/chart_view_line_chart3.png)

*Here, we added the Segment as the second level of grouping -  as a result, we have one line showing the evolution of each segment over the days*

### c. Specific settings for line charts

In the design section, you can access the following parameters, specific to line charts:

- _Align zero:_ If we have many different axis, this setting will determine whether or not to align all the 0 horizontally.

- _Fill in temporal gaps:_ If the X-Axis is a temporal one, date or date time, empty points will be added in case the dataset is missing dates. For example, if the dataset has a point for the 1/1/2020, and one for the 1/3/2020 - the chart will add a tick on the X-Axis on the 1/2/2020. 

For each series, you can also configure if you want to:

- Smooth the lines
- Draw an area beneath the lines
- Add a trend line (Polynomial or Linear)
- Change line width / line style


## 1.3 Configure a pie chart

In the data section, pick the Series and the Groupings.
A pie chart can have one or two levels of grouping and does not have any limit in the number of series.

> When adding more than one series, KAWA will create as many pie charts as series.

> Only show series containing positive values. Otherwise the pie chart can lead to misinterpretation of the data.


![Chart config](./readme-assets/chart_view_pie1.png)

*A simple pie chart showing the sales per state. A Pie chart will show the ten biggest categories and then aggregate all the others in an `Other` category*.


![Chart config](./readme-assets/chart_view_pie2.png)

*Make sure to select the Sunburst option in the settings tab for a pie chart with two levels of groupings*.

> When using more than one level of grouping on a pie chart, you should use the `SUM` aggregation.

The design tab offer special options for Pie charts:

- _Doughnut:_ Plots as a doughnut instead of a pie chart

- _Labels outside:_ Shows the labels outside of the chart. Can be more readable in some configurations.


# 2 Series and Groups

Series and Groups define what data will be plotted in the charts. They play different roles in different types of charts.


## 2.1 Chart series

![Chart config](./readme-assets/chart_view_fields.png)

Each field has several configuration options:

- _Display:_ You can configure the field name (how it will appear on the charts) as well as the format of labels associated with this field. (For example set a unit or a number of digits to show after the decimal point). All these parameters are accessible on the three dots menu of each field.

- _Aggregation:_ The charts will show aggregated values for each field. For example: The sum of profit per segment or The average of sales per region, etc... The first drop dow menu contains a list of aggregation to pick from.

> __IMPORTANT:__ Be mindful of the aggregation method when you are plotting time series with time sampling. It is recommended to use aggregations such as Average, Min or Max (and avoid SUM as the value will grow with the number of samples falling within each bucket).

- _Calculation:_ In charts, you can define ad-hoc calculations to apply to your fields by setting the Show As parameter.

__Table 1:__ Calculation Methods for one level of grouping:

| Calculation | Description   |     
|--------------------|---------------|
| Original Value     | Displays the aggregated value of each measure without any transformation.
| % of total         | Displays the percentage contribution of each aggregated value to the overall total.
| % of group         | For one level of grouping, behaves the same as the % of total.
| Cumulated          | Displays the running total, combining the current value with all previous ones.
| Difference with    | Displays the difference between the current value and the one before it. No value will be shown for the first data point.
| % of difference with    | Displays the difference between the current value and the one before it in proportion. No value will be shown for the first data point.
| % of previous value | Shows each point as the percentage of the previous one.


__Table 2:__ Calculation Methods for two levels of grouping:

| Calculation| Description   |     
|--------------------|---------------|
| Original Value     | Displays the aggregated value of each measure without any transformation.
| % of total         | Displays the percentage contribution of each aggregated value to the overall total, across all points.
| % of group         | Display the percentage contribution of each aggregated value within its parent group.
| Cumulated          | Displays the running total within each group, combining the current value with all previous ones, still within each group.
| Difference with    | Displays the difference between the current value and the one before it, in the same group. No value will be shown for the first data point.
| % of difference with    | Displays the difference between the current value and the one before it, within each group, in proportion. No value will be shown for the first data point.
| % of previous value | Shows each point as the percentage of the previous one in the same group.


__Moving calculations:__
Moving calculations can also be configured from within the Show As menu. 

- _Apply to:_ Defines the level of grouping to which you apply the calculation

- _Aggregation:_ Defines how to aggregate the data points together. This aggregation will be used to combine aggregated values together. (For example: the cumulative SUM of AVERAGES)

- _Previous Values:_ Specifies how many previous values to include, defined as a positive integer.

- _Next Values:_ Specifies how many next values to include, defined as a positive integer.

- _Current value:_ Specifies whether or not to include the current value.



![Chart config](./readme-assets/chart_view_sliding_avg.png)

_Above the result of using a moving calculation with: Apply to: Date, Aggregation: Average, Prev: 10, Next: 0, Current value: Yes. It computes the sliding average over the last 10 points._