---
layout: default
title: CSV Import
parent: Data Integration
nav_order: 4
---

# Import CSV

This is the most straightforward way to import data in KAWA.

* TOC
{:toc}

## 1. Importing a new CSV file

In order to import a new CSV file, from the __Data Source__ section, click on __(+ Data Source)__ then __(Upload a File)__.


### 1.1 Step 1 of 2: Select the data to import

In the first step, use the file picker on the right to drag and drop a file or select a file from your system.

The following formats are accepted:

- .csv
- .csv.gz
- .csv.zip

> 💡 It is recommended to use compressed csv formats when the volume of data exceeds 100MB.

### 1.2 Configure the CSV import parameters

Once the file has been loaded on KAWA and a preview has been generated, use the right pane to configure the import.

> ℹ️ Most of the time, no additional configuration will be required as KAWA tries to auto detect all the parameters.

Here are the available parameters:

| Parameter | Description
|-----------|------------
| Column Delimiter | Will define the delimiter used to separate columns. In the US or in the UK, it is often the comma. In France the semicolon is used.
| Quote Character | In a CSVfile, the quote character (usually a double quote ") is used to enclose field values that contain special characters such as: separators, new lines.
| Escape Character | Is used to escape the Quote characters withing the quoted values. For example if the quote character is `"` and the escape character is `\`: The following text is a valid value: `"She said: \"Hello\""`
| Decimal Separator | Delimits the whole number part from the fractional part in a numeric value. 
| Thousands Separator | The thousands separator divides large numbers into groups of three digits to improve readability.
| Date Format | Specifies the format of the dates
| Timestamp Format | Specifies the format of the date times
| Encoding | The default is UTF-8. If the CSV file comes from a Windows system and includes special characters like é or à, ensure the appropriate encoding is selected to display the characters correctly.
| Time Zone | Will assume that all date times without explicit Time Zone will be in the configured Time Zone.
| Header Row | Specifies the position of the header row in the CSV file. For example, a value of 1 indicates that the header is on the first line, 2 means it's on the second line, and so on.

