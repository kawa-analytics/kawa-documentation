---
title: Getting Started
nav_order: 2
---

# Getting started

KAWA contains 5 main sections:

* Connect your data in the **Data Source** section
* Build your models and explore in the **Sheet** section
* Automate actions and processes in the **Workflows** section
* Publish in the **Dashboard** and **Applications** sections

## 1. Create your first Data Source

Loading data into KAWA is the first step, and it is done via the Data Source section.

> If the data that you want to explore is already loaded in KAWA, go to the next paragraph.

Let's create one from a simple CSV file. This example will use a sample CSV file you can download - but feel free to bring in your own.

{% file src=".gitbook/assets/store.csv" %}

* _Step 1:_ Go to the Data Source section (Top icon in the left bar), and click on the **(+ Data Source)** button. Choose: **(Upload a file)**.

<div data-with-frame="true"><img src=".gitbook/assets/start10.png" alt=""></div>

* _Step 2:_ Drag and Drop your file in the drop zone and once your data is displayed, click on **(Next)**

<div data-with-frame="true"><img src=".gitbook/assets/start11.png" alt=""></div>

* _Step 3:_ Click directly on **(Save)**. In the form, choose a good name for your new Data Source, then click on **(Save and run)**.

<div data-with-frame="true"><img src=".gitbook/assets/start2.png" alt=""></div>

Your first Data Source has been created. The system will take a few seconds to process the entire file. Once it is done, you will see a green **SUCCESS** badge that indicates that the data has been successfully loaded.

Before going to the next paragraph, go ahead and click on the **Data** tab, next to overview. There, you will see the profile of your uploaded dataset.

<div data-with-frame="true"><img src=".gitbook/assets/start3.png" alt=""></div>

You can click on the various columns to get detailed information about them.

## 2. Create your first Sheet

There are two ways to create a Sheet on top of a Data Source.

* From the Data Source section, click on your Data Source and click on the **(Explore)** button at the top. You will be redirected it the new sheet.
* From the Sheet section (Second icon from the top in the left bar), click on the **(+ Sheet)** button, and select your Data Source. Click on **(Next)**, pick a name for your Sheet and **(Create)**.

A Sheet works like an Excel Workbook. When created, it has only one tab, which is the default Grid. This is the ideal tool to explore your data in KAWA.

### 2.1 Manipulate your data in the grid

Feel free to explore the main actions by using the buttons on the top right of the Grid.

<div data-with-frame="true"><img src=".gitbook/assets/start5.png" alt=""></div>

A good starting point is Grouping. Click on the **(Group)** button (on the top right), and on the **(+)** button. Choose the _State_ field (Or any other dimension of your dataset), and click on **(Apply)**.

<div data-with-frame="true"><img src=".gitbook/assets/start4.png" alt=""></div>

Feel free to explore: Sorting, Hide field, Filtering. All the options of the grid view are documented in details in the [Grid View section](04_00_visualization/04_01_grid_views.md). There is a special section about [Filtering](04_00_visualization/04_04_filtering.md).

### 2.2 Create a new simple formula

The **(Enrich Data)** button is the way to add data in your sheet to complement the one coming from your data source. It lets you join with other data sources (Lookup column), create ad-hoc mapping tables, create your own formulas and even connect to Python scripts.

Let's create a simple formula to compute the unit profit by dividing the _Profit_ by the _Quantity_.

> This is based on the example file from the first paragraph, feel free to adapt to your own business logic.

* _Step 1:_ Click on the **(Enrich Data)** button, then **(Formula)**.

<div data-with-frame="true"><img src=".gitbook/assets/start14.png" alt=""></div>

* _Step 2:_ If AI is enabled on your platform, you can just type: "Calculate unit profit". If it is not, just type `Profit / Quantity` (Do not copy paste, type in the formula). KAWA will assist you on the way.
* _Step 3:_ Type in a name for your formula and **(Create)**. The new column will be added in your grid, at the last position.

<div data-with-frame="true"><img src=".gitbook/assets/start6.png" alt=""></div>

### 2.3 Create a first simple chart

In order to explore your data in a more visual way, let's now create a chart. In our example, let's have a look at a profit trend over the years.

* _Step 1:_ On the top left, click on **(Create View)**, and pick **(Graph/Chart)**.

<div data-with-frame="true"><img src=".gitbook/assets/start13.png" alt=""></div>

* _Step 2:_ In the configuration panel, search for the _Profit_ column and drag and drop it in the Series Zone.
* _Step 3:_ In the configuration panel, search for the _Order Date_ column and drag and drop it in the Group by Zone.
* _Step 4:_ Next to the Order Date in the Group By Zone, click on the small Calendar and pick: **(Year/Month)**. This will sample the data by month.
* _Step 5:_ Click on the line chart icon.

<div data-with-frame="true"><img src=".gitbook/assets/start7.png" alt=""></div>

Please refer to the complete [Chart Documentation](04_00_visualization/04_02_chart_views.md) to learn how to customize your charts.

### 2.4 Create a Pivot Table

Pivot tables in KAWA work like in any spreadsheet software, except that they can scale on billions of rows.

* _Step 1:_ On the top left, click on **(Create View)**, and pick **(Pivot Table)**.

<div data-with-frame="true"><img src=".gitbook/assets/start12.png" alt=""></div>

* _Step 2:_ In the Rows section, add the _State_ column. This can be done either by drag and drop or by clicking on the **(+)** and selecting the State column.
* _Step 3:_ In the Columns section, add the _Segment_ column.
* _Step 4:_ In the Values section, add the _Sales_ column.

<div data-with-frame="true"><img src=".gitbook/assets/start8.png" alt=""></div>

To know what is possible with the pivot tables, go to the [Pivot Documentation](04_00_visualization/04_03_pivot_table_views.md).

## 3. Put it together in a Dashboard

Go to the **Dashboard** section (Third icon from the top in the left bar). Click on **(+ Dashboard)**, then **(Dashboard)**.

You will be redirected to a new empty dashboard. Pick your sheet from the **(Add Widgets)** panel and add the view you created in the previous steps.

Widgets can then be arranged in the layout of your choice. Dashboard are a powerful tool to bring data from all your sheets in one place.

<div data-with-frame="true"><img src=".gitbook/assets/start9.png" alt=""></div>

## 4. What's next?

Those three paragraphs: **Data Source**, **Sheet** and **Dashboard** are giving a good overview of the central structure of the KAWA platform. It is the base on which you can start building and sharing your data applications.

| Objective                                                    | Link                                                       |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| Connect your Python libraries to KAWA                        | [Python integration](09_00_python_integration/)            |
| Build and share data applications                            | [Publishing](05_00_publishing/)                            |
| Connect KAWA to your Jupyter notebook to load and query data | [Python SDK](09_00_python_integration/09_01_python_sdk.md) |
| Automate your workflows                                      | [Workflows](07_00_workflows/)                              |
| Use AI to chat with your data                                | [AI Integration](06_00_ai_integration.md)                  |
| Build and share data models                                  | [Data Modeling](02_00_modeling/)                           |
| Build impactful visualizations                               | [Visualizations](04_00_visualization/)                     |
