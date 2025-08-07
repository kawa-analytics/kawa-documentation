---
layout: fullwidth
title: Backup and Restore
parent: Exploitation
nav_order: 32
---

## Backup and Restore scripts

This section contains scripts to backup and restore your postgres and clickhouse databases.
It is compatible with a docker based installation, but can be adapted to work with bare metal setups.

* TOC
{:toc}

# 1. Backup and Restore the postgres Database

> ℹ️ Run these scripts from directory that contains the `docker-compose.yml`file.

## 1.1 Backup postgres

KAWA Postgres database contains all the state of the application - dashboards, applications, sheets, datasources, views, etc...
It also contains user accounts if using KAWA's internal authentication mechanism.

```bash
#!/bin/bash

DOCKER_CONTAINER_NAME="postgres"
DUMP_DIR="/tmp"
KAWA_COMPOSE_DIR="$PWD"
EXCLUDED_TABLE="application_event"
DB_USER="kawa"
DB_NAME="postgres"

TIMESTAMP=$(date +%Y-%m-%d)
DUMP_FILE="$DUMP_DIR/kawa-db-$TIMESTAMP.sql"
TAR_FILE="$DUMP_DIR/kawa-db-$TIMESTAMP.tar.gz"

mkdir -p "$DUMP_DIR"

echo "1️⃣ Starting database dump to $DUMP_FILE..."
if sudo docker compose exec "$DOCKER_CONTAINER_NAME" \
    pg_dump -U "$DB_USER" "$DB_NAME" --exclude-table-data="$EXCLUDED_TABLE" > "$DUMP_FILE"; then
  echo "✅ Database dump completed successfully."
else
  echo "❌ Database dump failed." >&2
  exit 1
fi

echo "2️⃣ Compressing dump to $TAR_FILE..."
if tar -czf "$TAR_FILE" -C "$DUMP_DIR" "$(basename "$DUMP_FILE")"; then
  echo "✅ Compression successful: $TAR_FILE"
  rm -f "$DUMP_FILE"
else
  echo "❌ Compression failed." >&2
  exit 1
fi
```


## 1.2 Restore the postgres database


```bash
#!/bin/bash

DOCKER_CONTAINER_NAME="postgres"
TAR_FILE_PATH="/tmp/kawa-db-$(date +%Y-%m-%d).tar.gz"
DB_USER="kawa"
DB_NAME="postgres"
TARGET_SCHEMA='kawa'
BACKUP_SCHEMA="kawa_backup_$(date +%Y%m%d)"


echo "1️⃣ Extracting SQL dump from $TAR_FILE_PATH..."
TEMP_DIR=$(mktemp -d)

if tar -xzf "$TAR_FILE_PATH" -C "$TEMP_DIR"; then
  DUMP_FILE=$(find "$TEMP_DIR" -name "*.sql")
  echo "✅ Extracted dump file: $DUMP_FILE"
else
  echo "❌ Failed to extract $TAR_FILE_PATH" >&2
  exit 1
fi

echo "2️⃣ Checking for existing '$TARGET_SCHEMA' schema..."
RENAME_SQL="
DO \$\$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = '$TARGET_SCHEMA') THEN
    EXECUTE 'DROP SCHEMA IF EXISTS $BACKUP_SCHEMA CASCADE';
    EXECUTE 'ALTER SCHEMA $TARGET_SCHEMA RENAME TO $BACKUP_SCHEMA';
  END IF;
END
\$\$;
"

echo "$RENAME_SQL" | sudo docker compose exec -T "$DOCKER_CONTAINER_NAME" \
  psql -U "$DB_USER" -d "$DB_NAME" || {
    echo "❌ Failed to rename existing schema." >&2
    rm -rf "$TEMP_DIR"
    exit 1
}


echo "3️⃣ Restoring dump into Docker container database..."
if cat "$DUMP_FILE" | sudo docker compose exec -T "$DOCKER_CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"; then
  echo "✅ Database restored successfully."
else
  echo "❌ Database restore failed." >&2
  rm -rf "$TEMP_DIR"
  exit 1
fi


rm -rf "$TEMP_DIR"
```



# 2. Backup and Restore the clickhouse Database

In order to backup and restore a clickhouse database, we use the native BACKUP and RESTORE utilities from Clickhouse.

Connect to your clickhouse database with a SQL client:
```sql
BACKUP DATABASE default TO Disk('backups', 'default.zip')
```

To restore a database:

```sql
 RESTORE DATABASE default FROM Disk('backups', 'default.zip')
 ```

The backups will be generated in the `assets/backup` directory of your docker compose install folder. Please refer to https://clickhouse.com/docs/operations/backup for additional configuration options and details.