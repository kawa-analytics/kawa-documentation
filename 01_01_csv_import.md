---
layout: default
title: CSV Import
parent: Data Integration
nav_order: 4
---

Import CSV
---

This is the most straightforward way to import data in KAWA.

* TOC
{:toc}

# 1 Importing a new CSV file

In order to import a new CSV file, from the __Data Source__ section, click on __(+ Data Source)__ then __(Upload a File)__.


## 1.1 Step 1 of 2: Select the data to import

In the first step, use the file picker on the right to drag and drop a file or select a file from your system.

The following formats are accepted:

- .csv
- .csv.gz
- .csv.zip

> 💡 It is recommended to use compressed csv formats when the volume of data exceeds 100MB.


### 1.1.1 Configure the CSV import parameters

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


### 1.1.2 Configure the import type

This is valid for most of the Data Sources, not limited to CSV imports.
Three options are available:

| Option | Description
|-----------|------------
| Reset Before Insert | Each time the import will run, the data in KAWA will be entirely replaced with the content of the file.
| Incremental | The data from the incoming file will be appended to the data that was already imported. Based on the primary key, if some rows that were already present in KAWA are present in the file, then the values will be replaced.
| Snapshot | This mode will append all the content of the file to the existing data. Two additional columns will be created: `Snapshot Id` and `Snapshot DateTime`. 

Please refer tpo the three examples below:


#### a. Reset Before Insert

__1️⃣ Initial import:__

| 🔑 Stock | Position
|-------|----------
| WAYNE | 23
| WONKA | 12

Data in KAWA after initial import:

| 🔑 Stock | Position
|-------|----------
| WAYNE | 23
| WONKA | 12


> The data will be copied in KAWA after the initial import, exactly as is.

__2️⃣ Second import:__

| 🔑 Stock | Position
|-------|----------
| WAYNE | 25
| STARK | 26

Data in KAWA after second import:

| 🔑 Stock | Position
|-------|----------
| WAYNE | 25
| STARK | 26

In the Reset Before Insert mode, the data is deleted in KAWA before importing the new position. As a result, KAWA will contain exactly a copy of the second import. My position on WONKA will be removed and a new position on STARK will be added.


#### b. Incremental

__1️⃣ Initial import:__

| 🔑 Stock | Position
|-------|----------
| WAYNE | 23
| WONKA | 12

Data in KAWA after initial import:

| 🔑 Stock | Position
|-------|----------
| WAYNE | 23
| WONKA | 12


> The data will be copied in KAWA after the initial import, exactly as is.

__2️⃣ Second import:__

| 🔑 Stock | Position
|-------|----------
| WAYNE | 25
| STARK | 26

Data in KAWA after second import:

| 🔑 Stock | Position
|-------|----------
| WAYNE | 25
| WONKA | 12
| STARK | 26

In the incremental mode, the content of the second import will be appended to the existing data. This explains why the STARK position is added, and why the WONKA position is not affected. Because the WAYNE stock was already present, its value will be updated (The initial 23 will be replaced with a 25).



#### c. Snapshot



__1️⃣ Initial import:__

| 🔑 Stock | Position
|-------|----------
| WAYNE | 23
| WONKA | 12

Data in KAWA after initial import:

| 🔑 Stock | Position | 🔑 Snapshot id | 🔑 Snapshot date time
|----------|-----------|-------------|-----------------------
| WAYNE | 23         | 1 | 2025-25-06 12:34:56
| WONKA | 12         | 1 | 2025-25-06 12:34:56

> Two additional columns will be added: `snapshot id` and `snapshot date time`, both of these will be added to the existing primary keys. For the first import, because we are realing
