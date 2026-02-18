---
title: Python SDK
parent: Python Integration
nav_order: 30
---

# Python SDK

KAWA offers a Python SDK that lets you perform various operations: Computations, Data loading and Advanced administration tasks.

You can find example workbooks and additional documentation here: [KAWA Python SDK Github Repository](https://github.com/kawa-analytics/kywy-documentation).

## 1. Getting started with the SDK

### 1.1 Installation

In order to install the SDK, run the following:

`pip install kywy`

> The SDK is hosted on [PyPI](https://pypi.org/project/kywy/).

### 1.2 Retrieve your API Key

The API Key can be retrieved from the KAWA GUI. Click on **Settings** > **API Key**.

Please set a date at which the key will expire and click on **Generate key**.

The key is of the following format:

```
kawa-........
```

> Once generated and copied, the key can no longer be retrieved. If you lost you key, you will need to generate a new one.

### 1.3 Connect and authenticate to KAWA

The recommended way to connect to KAWA with the Python SDK is by creating a `.env` file in your project root directory.

> The `.env` file will be located by searching upward from the current working directory until the file is found or the root directory is reached.

Here is what the content of your `.env` file should look like:

```bash
KAWA_URL=https://your-domain:your-port
KAWA_API_KEY=kawa-****
KAWA_WORKSPACE=1
```

Specify the following:

* _KAWA\_URL:_ Enter your URL with the correct port
* _KAWA\_API\_KEY:_ Fill in the API key that was generated at the previous step
* _KAWA\_WORKSPACE:_ Specify in which workspace you want to be authenticated

When the file has been created, run the following:

```python
from kywy.client.kawa_client import KawaClient as K
kawa = K.load_client_from_environment()
```

Alternatively, you can authenticate without using the `.env` file (not recommended):

```python
from kywy.client.kawa_client import KawaClient as K
kawa = K(kawa_api_url='https://your-domain:your-port')
kawa.set_api_key(api_key='kawa-****')
kawa.set_active_workspace_id('1')
```

## 2. Upload data to KAWA using the Python SDK

In order to upload any pandas dataframe to KAWA:

```python
from kywy.client.kawa_client import KawaClient as K
kawa = K.load_client_from_environment()

# Define your dataframe
# df = ....

loader = kawa.new_data_loader(
    df=df, 
    datasource_name='Super Store',
)

loader.create_datasource()
loader.load_data()
```

Please have a look at this [Notebook](https://github.com/kawa-analytics/kywy-documentation/blob/main/notebooks/data-operations/01_load_data_notebook.ipynb) for a complete documentation of the data loading API.

> Note that you can also use arrow tables instead of pandas dataframe for improved performances. This is all detailed in the notebook mentioned above.

## 3. Run computations on KAWA from the Python SDK

This feature lets you query your data and download it as a pandas dataframe directly in your existing scripts. The execution of the query (Filtering, Aggregations, etc...) will be deported into the KAWA data warehouse to ensure low latency and a small memory footprint in your own Python runtime.

```python
from kywy.client.kawa_client import KawaClient as K
kawa = K.load_client_from_environment()

query = (kawa
         .sheet('Super Store')
         .select(K.col('Profit').sum())
         .group_by('State')
         .order_by('Profit', ascending=False)
         .limit(5))

df = query.compute()

# df is a regular Pandas dataframe that can be further manipulated.
```

Please have a look at this [Notebook](https://github.com/kawa-analytics/kywy-documentation/blob/main/notebooks/data-operations/02_compute_notebook.ipynb) for a complete documentation of the computing API.
