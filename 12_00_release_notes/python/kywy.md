# kywy

`kywy` is the KAWA Python SDK: load data into KAWA, query sheets, and write the Python tools that workflows run. See [Python SDK](../../09_00_python_integration/09_01_python_sdk.md).

```
pip install --upgrade kywy
```

The versions are listed newest first.

## 0.37.11

**Release date:** 12 November 2026

* **Queries** — two aggregations are added on a column: `concat_unique()` and `concat_unique_not_empty()`.

## 0.37.10

**Release date:** 12 October 2026

* **Playbooks** — the agent run of a playbook is recorded in KAWA's agent telemetry.

## 0.37.9

**Release date:** 7 October 2026

* **Data loader** — an auto-increment column is a 64-bit integer when the data is loaded through Parquet. It was 32-bit.

## 0.37.8

**Release date:** 29 September 2026

* **Playbooks** — a playbook exposes its prompt and its skills on the tool.

## 0.37.7

**Release date:** 18 September 2026

* **Queries** — the same expression can be used in several queries.

## 0.37.6

**Release date:** 18 September 2026

* **Queries** — an inline expression finds a column by its immutable tag as well as by its display name.
* **Queries** — `collect()` works again without a request id.

## 0.37.4

**Release date:** 11 September 2026

* **Queries** — each computation carries a request id.
* **Playbooks** — output tables are written as JSON Lines, one row per line.

## 0.37.3

**Release date:** 6 September 2026

* **Data loader** — general improvements to the loader.
* **Data loader** — an Arrow table with no rows loads as an empty datasource.
* **Data loader** — an upload to Databricks no longer times out.

## 0.37.1

**Release date:** 19 July 2026

* **Playbooks** — the `kawa_playbook` decorator: an agent-powered tool written as a declaration.

## 0.37.0

**Release date:** 19 July 2026

* **Tools** — the `kawa_workflow_tool` decorator, a new way to declare a workflow tool.
