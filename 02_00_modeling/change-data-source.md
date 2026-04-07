# Change Data Source

The **Change data source** feature lets you replace the main data source of an existing sheet from the **Model** tab.

You can start this flow on an existing sheet even after you have already configured elements such as charts, pivot tables, grouping, filters, formulas, lookup columns, and mapping columns.

## 1. Before you start

Important notes:

* The feature is available from the **Model** tab of a sheet.
* It is not available for **multi-sheets**.
* The current data source is shown in the dialog for reference.
* The current data source does not appear in the selection list.
* Any supported KAWA data source type can be used.
* Returning a sheet to its original data source after switching away from it is currently not supported.

## 2. Open the Change data source dialog

1. Open the sheet.
2. Go to the **Model** tab.
3. Click **Change data source** in the toolbar.

<figure><img src="../.gitbook/assets/change_data_source1.png" alt=""><figcaption></figcaption></figure>

_Change Data Source is available from the Model tab of a sheet._

KAWA opens a 3-step dialog:

1. **Select source**
2. **Map columns**
3. **Review**

## 3. Step 1 — Select source

In the first step, KAWA shows:

* the current data source
* a searchable list of available replacement data sources
* the number of columns in each source
* whether a source is incompatible
* how many additional columns will be added to the sheet

Data sources with fewer columns than the current one appear as **incompatible**.

Select the new data source and click **Next**.

<figure><img src="../.gitbook/assets/change_data_source2.png" alt=""><figcaption></figcaption></figure>

_Select a replacement data source and review compatibility before continuing._

## 4. Step 2 — Map columns

In the mapping step, every column from the current main data source must be mapped to one column in the new data source.

KAWA automatically matches columns when their **name** and **type** match.

Rules for mapping:

* all current-source columns must be mapped before you can continue
* columns of different types cannot be mapped to each other
* the same new column cannot be mapped to multiple current columns
* the mapping must be **1:1**

If the new data source contains additional columns that are not used in the mapping, those columns are added to the sheet automatically.

After completing the mapping, click **Next**.

<figure><img src="../.gitbook/assets/change_data_source3.png" alt=""><figcaption></figcaption></figure>

_Map each current column to a matching column in the new data source._

## 5. Step 3 — Review

In the review step, KAWA shows:

* the current data source and the new data source
* the number of mapped columns
* the list of new columns that will be added to the sheet

Review the change carefully before applying it.

> New columns will be added to the sheet. This action cannot be undone.

Click **Apply** to update the sheet model.

<figure><img src="../.gitbook/assets/change_data_source4.png" alt=""><figcaption></figcaption></figure>

_Review the selected source, mapped columns, and new columns before applying the change._

## 6. Example

Suppose your sheet is currently based on `cities_basic.csv` with the following columns:

* `id`
* `city`

You change the sheet to `cities_with_population.csv`, which contains:

* `id`
* `city`
* `population`

In this case:

* `id` is mapped to `id`
* `city` is mapped to `city`
* `population` is added to the sheet automatically

For example, the original data source may look like this:

| id | city       |
| -- | ---------- |
| 1  | Amsterdam  |
| 2  | Berlin     |
| 3  | Copenhagen |
| 4  | Dublin     |
| 5  | Edinburgh  |

The new data source may look like this:

| id | city       | population |
| -- | ---------- | ---------- |
| 1  | Amsterdam  | 921402     |
| 2  | Berlin     | 3644826    |
| 3  | Copenhagen | 667099     |
| 4  | Dublin     | 592713     |
| 5  | Edinburgh  | 506520     |

After the change:

* `id` remains mapped to `id`
* `city` remains mapped to `city`
* the new `population` column is added to the sheet automatically

<figure><img src="../.gitbook/assets/change_data_source5.png" alt=""><figcaption></figcaption></figure>
