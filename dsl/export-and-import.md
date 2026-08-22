# Inventory, export and import

Moving a workspace — or part of one — rests on **three commands**, and nothing else:

| Command | What it does |
| --- | --- |
| [`kawa inventory`](#1-inventory-what-a-workspace-holds) | Lists every entity in a workspace with its **immutable tag** — the identity you select with, and the only correct way to name an entity |
| [`kawa export`](#2-export-from-a-workspace) | Snapshots a workspace, or a tag-selected part of it, into a single portable ZIP |
| [`kawa import`](#3-load-an-export-into-another-workspace) | Applies that ZIP to any workspace, on any KAWA server |

They compose in one direction — **inventory → export → import**:

```bash
kawa inventory --workspace-id=12                       # 1. find the tags
kawa export --workspace-id=12 --output=source.zip      # 2. snapshot the source
kawa import source.zip --workspace-id=77 --plan-only   # 3. dry run on the target
kawa import source.zip --workspace-id=77 --yes         #    apply
```

Typical uses: cloning a workspace for a new team, moving a proven build from a sandbox instance to production, seeding a demo environment, or archiving a definition outside KAWA.

All three need only the [connection variables](README.md#connect) — `KAWA_API_URL` and `KAWA_API_KEY`. None of them requires a checkout or a local working directory.

## 1. Inventory: what a workspace holds

```bash
kawa inventory --workspace-id=12
```

It reads the live server and prints one block per kind — scripts, datasources, sheets, dashboards, workflows, agents, applications, artifacts, skills — with each entity's name, immutable tag, creation date, owner and description:

```
SCRIPTS (2)
  NAME                TAG                             CREATED     OWNER  DESCRIPTION
  send_slack_message  send-slack-message_89f510f5a656  2026-04-21  1

SHEETS (27)
  NAME       TAG                   CREATED     OWNER  DESCRIPTION
  Clients    clients_384109515a8e  2026-04-21  1
  ...
```

`--workspace-id` is optional inside a directory already bound to a workspace; that workspace is the default.

**This is where tags come from.** A tag is an opaque string — never assemble one from a display name, never edit one by hand, never assume the part before the underscore means anything. Copy it from this listing (or from `--json`) into `kawa export --tags=…`.

`--json` emits the same inventory as a machine-readable document, keyed by kind, one object per entity:

```json
{
  "sheets": [
    {
      "name": "Clients",
      "description": "",
      "tag": "clients_384109515a8e",
      "created": "2026-04-21",
      "owner": "1"
    }
  ]
}
```

### Inventory options

| Flag | Effect |
| --- | --- |
| `--workspace-id=<id>` | Workspace to inventory (default: the bound workspace) |
| `--json` | Machine-readable output instead of the tables |

## 2. Export from a workspace

### The whole workspace

```bash
kawa export --workspace-id=12
```

`--workspace-id` is optional if you run from a directory already bound to a workspace (after `kawa checkout 12`) — that workspace is the default. With neither, the command stops and tells you so.

The bundle lands in the current directory as `<workspace-name>-<YYYYMMDD>.zip` unless you choose otherwise. `--output` accepts a file path or a directory:

```bash
kawa export --workspace-id=12 --output=./bundles/           # directory → default name inside it
kawa export --workspace-id=12 --output=prod-snapshot.zip    # exact file name
```

A successful run ends with a single line:

```
Exported workspace 'Sales Analytics' → /path/sales-analytics-20260822.zip (2,163 bytes, data=yes)
```

Overwriting an existing file requires `--force`, so a bundle you still need is never silently replaced.

### Exporting only part of a workspace

Entities are selected by their **immutable tag** — [`kawa inventory`](#1-inventory-what-a-workspace-holds) is where you read them. Export what you need:

```bash
kawa export --workspace-id=12 --tags=clients_384109515a8e --output=clients.zip
```

The export automatically adds the **dependency closure** — everything the selection needs in order to import cleanly:

| You select | The bundle also carries |
| --- | --- |
| a sheet | its datasource, its views |
| a view | its sheet, and that sheet's datasource |
| a dashboard | every sheet it displays, and their datasources |
| a workflow | the scripts and sub-workflows it runs |

The command reports what the closure came to:

```
Selection: 1 datasource(s), 1 sheet(s), 1 view(s)
```

Use `--no-deps` to take **exactly** the named entities and nothing else. That is for a target which already holds every dependency: the entities are matched there by tag and updated in place.

```bash
kawa export --workspace-id=12 --tags=sales_ab12cd34ef --no-deps --output=one-dashboard.zip
```

### Export options

| Flag | Effect |
| --- | --- |
| `--workspace-id=<id>` | Workspace to export (default: the bound workspace) |
| `--output=<path>` | ZIP path or directory (default: `./<name>-<date>.zip`) |
| `--tags=<tag,tag>` | Export only these entities plus their dependency closure |
| `--no-deps` | With `--tags`: exactly those entities, no closure |
| `--no-data` | Schema only — do not include editable-datasource rows |
| `--force` | Overwrite the output file if it already exists |

### What a bundle contains

```
clients.zip
├── manifest.json                                  ← source workspace, counts, selection
└── src/
    ├── dsl/datasources/clients_16a2d90d8b22.toml
    ├── dsl/sheets/clients_384109515a8e.toml
    ├── dsl/views/clients_2513ea4a1adc.toml
    └── data/clients_16a2d90d8b22.csv              ← editable rows (omitted with --no-data)
```

A full-workspace bundle also carries dashboards, workflows, agents and applications under `src/dsl/`, script sources under `src/scripts/`, and file-datasource blobs under `src/files/`.

`manifest.json` records where the bundle came from, and — for a partial export — both the tags you asked for and the closure that was resolved:

```json
{
  "kind": "kawa-workspace-export",
  "schema_version": 1,
  "source_workspace_id": "12",
  "source_workspace_name": "Sales Analytics",
  "include_data": true,
  "entity_counts": { "datasources": 1, "sheets": 1, "scripts": 0, "dashboards": 0, "workflows": 0 },
  "selection": {
    "requested_tags": ["clients_384109515a8e"],
    "closure_tags": ["clients_16a2d90d8b22", "clients_2513ea4a1adc", "clients_384109515a8e"],
    "follow_deps": true
  }
}
```

> **Note:** a bundle is safe to hand to someone else — secrets and per-user settings are never written into it. Each environment supplies its own credentials when the bundle is imported.

### What cannot be exported

Some datasources have no portable representation. Rather than produce a bundle that cannot be imported, the export stops and names them:

```
Error: this workspace has datasource(s) that can't be exported:
  - Sales JDBC (kind=jdbc, adapter=postgres)
Provider-backed (JDBC/etc.), forbidden-file (read_only), and client-data
datasources can't be bundled portably.
```

Two ways forward:

* Export a **selection** that does not reach them (`--tags=…`) — the check runs after the selection is narrowed, so an unexportable datasource elsewhere in the workspace does not block you.
* Recreate the connection on the target instance, then import the rest.

Datasources fed by user uploads are converted to **editable** datasources on the way out, so their schema and their rows do travel.

## 3. Load an export into another workspace

### Step 1 — create the target workspace

The import applies a bundle to a workspace that already exists; it never creates one. Create it in the KAWA interface first, and note its id.

An empty, freshly created workspace is the cleanest target — and the one covered by KAWA's nightly test suite, which imports a bundle into a new workspace, exports it again, and requires the two definitions to be identical.

### Step 2 — dry run

```bash
kawa import source.zip --workspace-id=77 --plan-only
```

Nothing is applied. You see exactly what the real run would do:

```
Importing "Sales Analytics" into workspace 77 ...
No state file found. All resources will be created.
  + create datasource "Clients"
  + create sheet "Clients"

Plan: 2 to create.
```

Two things to read correctly:

* **Views are applied together with their sheet**, so a bundle carrying a sheet and its view shows up as one entity in the plan, not two.
* **Column-reference warnings** — `column reference "…" is not a known tag or name` — are expected against an empty workspace: the referenced entity does not exist *yet*. They are validated for real when the change is applied.

### Step 3 — apply

```bash
kawa import source.zip --workspace-id=77          # asks: Apply this plan? [y/N]
kawa import source.zip --workspace-id=77 --yes    # unattended
```

The run finishes with:

```
Seeded editable data into 1 datasource(s).
Import complete → workspace 77.
```

### Importing onto a different server

Bundles carry no server-specific identifiers, so the same file imports anywhere. Point the import at the target explicitly:

```bash
kawa import source.zip --workspace-id=77 \
  --url=https://other-kawa.mycompany.com \
  --api-key=<target api key> --yes
```

Without those flags the import uses `KAWA_API_URL` and `KAWA_API_KEY` — that is, it imports into the server you are already connected to.

### Import options

| Flag | Effect |
| --- | --- |
| `--workspace-id=<id>` | **Required.** Target workspace |
| `--url`, `--api-key` | Target server (default: the connected one) |
| `--plan-only` | Show the plan and stop — nothing is applied |
| `--yes` | Apply without the confirmation prompt |
| `--no-data` | Skip loading editable rows from the bundle |
| `--keep-work-dir` | Keep the extracted working directory for inspection |

The bundle argument accepts a `kawa export` ZIP, a template bundle, or an already-extracted directory.

### Importing into a workspace that is not empty

Supported. The import creates what is missing and updates what it finds by immutable tag; **it never deletes anything**. Run `--plan-only` first: the plan of a freshly extracted bundle describes what the bundle contains, so read it as the incoming definition rather than as a diff.

> **Note:** a large import can take several minutes. Bundles legitimately carry long-running data loads, and the import waits for them rather than timing out — it is working, not stuck.

### Verify

```bash
kawa inventory --workspace-id=77
```

Every entity should be present with the same tags as the source. For a strict check, re-export the target and compare the two bundles.

## Troubleshooting

| Message | What it means |
| --- | --- |
| `Error: no workspace to export.` | Neither `--workspace-id` nor a bound workspace directory. Pass the id. |
| `Error: … already exists. Use --force to overwrite.` | The output file is already there — rename it or pass `--force`. |
| `Error: this workspace has datasource(s) that can't be exported:` | A provider-backed, read-only-file, or client-data datasource. Select around it, or recreate it on the target. |
| `Error: --no-deps requires --tags.` | `--no-deps` only narrows an explicit selection. |
| An unknown tag in `--tags` | The tag does not exist in that workspace. Copy it from `kawa inventory` — tags are opaque and must never be typed by hand. |
| `Error: no src/ tree (dsl/ missing) under: …` | The file is not a KAWA bundle. Check the path. |
| `Nothing to import — target already matches the bundle.` | There is nothing to apply; the target already holds that definition. |

## Related

* [DSL overview](README.md) — install, connect, and the plan/commit cycle.
* [SDLC — governed delivery](../sdlc.md) — when transfers between environments need review, approval, and an audit trail rather than a one-off bundle.
