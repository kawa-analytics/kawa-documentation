# BigQuery native connection

## 1. Overview

KAWA's native connection to **Google BigQuery** allows organizations to leverage BigQuery as KAWA's data warehouse. KAWA's computation engine sits directly on top of a live BigQuery deployment — every query KAWA generates runs in BigQuery, against the customer's actual datasets. There is no extraction, no copy, and no separate analytics store.

This unlocks the full set of KAWA capabilities — Python-based ETL, dynamic schema augmentation, and real-time insights — orchestrated entirely within the customer's BigQuery environment. KAWA inherits BigQuery's elastic compute and storage, IAM model, and data residency.

KAWA connects to BigQuery using **Google's official `google-cloud-bigquery` Java client** (the first-party native SDK). The only secret KAWA ever needs is a **GCP service account JSON key**.

> If instead you want to use BigQuery only as an ingestion **source** (KAWA extracts data from BQ and loads it into a different KAWA warehouse such as ClickHouse), configure it as a regular datasource through the KAWA UI rather than following this guide.

## 2. Configuration guide

### 2.1 Configuring BigQuery

KAWA uses two distinct service accounts:

* A **write-back** account, used by KAWA to create and write its internal tables (user uploads, pandas DataFrame outputs, materializations, etc.) inside a dataset dedicated to KAWA.
* A **read-only** account, used by KAWA to query the customer's existing datasets across one or more GCP projects.

The two can be the same account with broader IAM, but separating them is recommended.

#### **a. Creating a project and dataset for KAWA to write in**

KAWA needs a dedicated **dataset** (the BigQuery equivalent of a Snowflake schema) where it will store its own tables. This dataset can live in any GCP project — typically the same project as the rest of the customer's BigQuery footprint.

```bash
PROJECT_ID=<your-project-id>

bq --project_id=${PROJECT_ID} mk \
  --dataset \
  --description="KAWA internal write-back dataset" \
  ${PROJECT_ID}:kawa_analytics
```

#### **b. Create a service account and role for KAWA's write-back account**

This account writes KAWA-managed tables into the `kawa_analytics` dataset created above.

```bash
PROJECT_ID=<your-project-id>
WRITER_SA=kawa-write-back@${PROJECT_ID}.iam.gserviceaccount.com

# Create the service account
gcloud iam service-accounts create kawa-write-back \
  --display-name="KAWA write-back" \
  --project=${PROJECT_ID}

# Allow it to run jobs in the project
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${WRITER_SA}" \
  --role="roles/bigquery.jobUser"

# Allow it to create / read / write tables in the kawa_analytics dataset
bq --project_id=${PROJECT_ID} add-iam-policy-binding \
  --member="serviceAccount:${WRITER_SA}" \
  --role="roles/bigquery.dataEditor" \
  ${PROJECT_ID}:kawa_analytics

# Generate the JSON key
gcloud iam service-accounts keys create kawa-write-back-key.json \
  --iam-account=${WRITER_SA}
```

The resulting `kawa-write-back-key.json` is the only secret KAWA needs for write-back.

**c. Create a service account and role with read-only access to the customer's data**

This account is used by KAWA to query the customer's datasets. Grant it `roles/bigquery.dataViewer` on each dataset KAWA users should be able to query, and `roles/bigquery.jobUser` on each project KAWA will run queries in.

> **DO NOT GRANT ANY OTHER PERMISSIONS BESIDES `dataViewer` AND `jobUser`** to this service account. The read-only account should only be able to query — never write or modify data outside the dedicated `kawa_analytics` dataset.

```bash
PROJECT_ID=<your-project-id>
READER_SA=kawa-readonly@${PROJECT_ID}.iam.gserviceaccount.com

# Create the service account
gcloud iam service-accounts create kawa-readonly \
  --display-name="KAWA read-only" \
  --project=${PROJECT_ID}

# Allow it to run queries in each project KAWA should query
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${READER_SA}" \
  --role="roles/bigquery.jobUser"

# Grant dataViewer on each dataset KAWA users should query
bq --project_id=${PROJECT_ID} add-iam-policy-binding \
  --member="serviceAccount:${READER_SA}" \
  --role="roles/bigquery.dataViewer" \
  ${PROJECT_ID}:<dataset_to_expose>

# Generate the JSON key
gcloud iam service-accounts keys create kawa-readonly-key.json \
  --iam-account=${READER_SA}
```

If KAWA should query datasets across **multiple GCP projects**, repeat the `jobUser` and `dataViewer` bindings for each project, and list every project in `KAWA_BIGQUERY_READER_PROJECT_LIST` (see below).

***

#### 2.2 Configuring KAWA

KAWA reads its BigQuery configuration from the secret store at startup. The following keys must be set as environment variables on the KAWA backend container, **or pulled from a managed secret store** — KAWA supports:

* **Google Secret Manager** (recommended when KAWA is deployed on GCP — keeps the BigQuery JSON keys inside the same trust boundary as BigQuery itself)
* **AWS Secrets Manager** (for KAWA on AWS)
* **Azure Key Vault** (for KAWA on Azure)
* **HashiCorp Vault** (cloud-agnostic — recommended for on-prem and multi-cloud deployments)
* Plain Kubernetes / environment variables for POC and development setups

In every case the secret **names** (e.g. `KAWA_BIGQUERY_READER_JSON_KEY`) and **values** are the same — only the storage backend changes.

**Read-only account:**

* `KAWA_BIGQUERY_READER_JSON_KEY` — the full contents of `kawa-readonly-key.json` as a single-line JSON string.
* `KAWA_BIGQUERY_READER_PROJECT_LIST` — _optional_ — comma-separated list of GCP project IDs the reader is allowed to query. Defaults to the project named in the JSON key.

**Write-back account:**

* `KAWA_BIGQUERY_WRITER_JSON_KEY` — the full contents of `kawa-write-back-key.json` as a single-line JSON string.
* `KAWA_BIGQUERY_WRITER_DATASET` = `kawa_analytics`
* `KAWA_BIGQUERY_WRITER_TABLE_PREFIX` = `KW__`

The writer account always operates on the **project named in its own JSON key** — it does not need a project list.

**Example — environment variables**

```bash
# Common: BigQuery configuration
KAWA_BIGQUERY_READER_JSON_KEY='{"type":"service_account","project_id":"...","client_email":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"}'
KAWA_BIGQUERY_READER_PROJECT_LIST='analytics-prod,analytics-staging'

KAWA_BIGQUERY_WRITER_JSON_KEY='{"type":"service_account","project_id":"...","client_email":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"}'
KAWA_BIGQUERY_WRITER_DATASET='kawa_analytics'
KAWA_BIGQUERY_WRITER_TABLE_PREFIX='KW__'
```

JSON keys are passed as **single-line JSON strings**. The GCP-issued JSON already escapes newlines in `private_key` with `\n`, so no manual escaping is required.

**Example — Google Secret Manager**

When KAWA runs on GCP, the JSON keys can be stored in **Google Secret Manager** instead of being passed as plain env vars:

```bash
PROJECT_ID=<your-project-id>

# Store each JSON key as a secret
gcloud secrets create KAWA_BIGQUERY_READER_JSON_KEY \
  --data-file=kawa-readonly-key.json \
  --project=${PROJECT_ID}

gcloud secrets create KAWA_BIGQUERY_WRITER_JSON_KEY \
  --data-file=kawa-write-back-key.json \
  --project=${PROJECT_ID}

# Grant the KAWA backend's service account access to read them
gcloud secrets add-iam-policy-binding KAWA_BIGQUERY_READER_JSON_KEY \
  --member="serviceAccount:kawa-backend@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding KAWA_BIGQUERY_WRITER_JSON_KEY \
  --member="serviceAccount:kawa-backend@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

KAWA fetches the secrets by name at startup and uses them exactly as if they had been provided via environment variables.

**Other backends**

The same pattern applies to **AWS Secrets Manager**, **Azure Key Vault**, and **HashiCorp Vault** — store each `KAWA_BIGQUERY_*` key as a named secret, grant the KAWA backend's identity access to read it, and KAWA will resolve it transparently. HashiCorp Vault is the recommended option for on-prem and multi-cloud deployments where a single secret store needs to serve KAWA regardless of where it runs.

> Workload Identity Federation (using GCP-side identity instead of a long-lived JSON key) is **not currently supported** — KAWA expects a JSON key.
