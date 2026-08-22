# Inventory, export and import

Moving a workspace — or part of one — rests on **three commands**, and nothing else:

| Command | What it does |
| --- | --- |
| [`kawa inventory`](#1-inventory-what-a-workspace-holds) | Lists every entity in a workspace with its **immutable tag** — the identity you select with, and the only correct way to name an entity |
| [`kawa export`](#2-export-from-a-workspace) | Snapshots a workspace, or a tag-selected part of it, into a single portable ZIP |
| [`kawa import`](#3-load-an-export-into-another-workspace) | Applies that ZIP to any workspace, on any KAWA server — an existing one, or one it creates for you |

`kawa import --test-stability` adds a fourth, optional step: after applying, [verify](#4-verify-a-bundle-with---test-stability) that the result exports back to the same definition.

They compose in one direction — **inventory → export → import**:

```bash
kawa inventory --workspace-id=12                       # 1. find the tags
kawa export --workspace-id=12 --output=source.zip      # 2. snapshot the source
kawa import source.zip --workspace-id=77 --plan-only   # 3. dry run on the target
kawa import source.zip --workspace-id=77 --yes         #    apply
kawa import source.zip --create-workspace --yes        #    …or into a brand-new workspace
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

### Step 1 — choose the target workspace

Every import needs a target, given one of two ways — you must pass exactly one:

```bash
kawa import source.zip --workspace-id=77       # into an existing workspace
kawa import source.zip --create-workspace      # into a new one, created for you
```

`--create-workspace` makes the workspace before importing, names it after the bundle plus a
timestamp, and prints it:

```
Created workspace "source 2026-08-22 17:26:09" (id=9270)
```

The timestamp matters: workspace names are not unique in KAWA, and repeatedly importing the same
bundle otherwise leaves you with a list of identical entries you cannot tell apart.

An empty, freshly created workspace is the cleanest target — and the one covered by KAWA's nightly
test suite, which imports a bundle into a new workspace, exports it again, and requires the two
definitions to be identical. `--create-workspace` is the one-flag version of that setup, and what
you want whenever you are evaluating an unfamiliar bundle rather than updating a known workspace.

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

The run finishes by naming where the content landed — not just the id:

```
Seeded editable data into 1 datasource(s).
Import complete → workspace "Sales Analytics" (id=77).
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
| `--workspace-id=<id>` | Target workspace. **Required unless** `--create-workspace` is given |
| `--create-workspace` | Create a new workspace (named `<bundle> <timestamp>`) and import into it. Mutually exclusive with `--workspace-id` |
| `--url`, `--api-key` | Target server (default: the connected one) |
| `--plan-only` | Show the plan and stop — nothing is applied |
| `--test-stability` | After importing, run the stability battery on the bundle. Mutually exclusive with `--plan-only` |
| `--yes` | Apply without the confirmation prompt |
| `--no-data` | Skip loading editable rows from the bundle |
| `--keep-work-dir` | Keep the extracted working directory for inspection |

The bundle argument accepts a `kawa export` ZIP, a template bundle, or an already-extracted directory.

### Importing into a workspace that is not empty

Supported. The import creates what is missing and updates what it finds by immutable tag; **it never deletes anything**.

Run `--plan-only` first. The import reads the target's current state before planning, so the plan is a **true diff** — entities the target already holds by tag show up as updates, not as creates, and a target that already matches produces no plan at all.

> **Note:** a large import can take several minutes. Bundles legitimately carry long-running data loads, and the import waits for them rather than timing out — it is working, not stuck.

### Verify

```bash
kawa inventory --workspace-id=77
```

Every entity should be present with the same tags as the source. That confirms the import *ran*.
For a strict check — that the result is a definition you can export and re-apply — use the
stability battery below.

## 4. Verify a bundle with `--test-stability`

An import exiting `0` tells you the bundle **applied**. It does not tell you the result can be
exported again and re-applied to the same shape — which is the question you actually have after
importing an unfamiliar bundle, and the property every promotion between environments depends on.

`--test-stability` answers it in the same run:

```bash
kawa import source.zip --create-workspace --yes --test-stability
```

It imports as usual, then runs the same battery as [`kawa test stability`](#the-same-battery-on-its-own) — one definition of "stable" for both commands. Three steps, in order, failing fast:

| Step | What it checks | How |
| --- | --- | --- |
| **0. Content scorecard** | The bundle is well-formed | Static, no server: counts entities, tombstones and lookups, and hard-fails on two known regressions — a `\|\|`-concatenation formula leak, and bare-numeric cross-entity references (raw ids that are not portable between servers) |
| **1. Determinism** | Reading a workspace gives the same answer twice | Exports the imported workspace **twice** and requires the two trees to be byte-identical |
| **2. Fixed point** | Writing then reading round-trips | Applies that export to a **fresh scratch workspace**, exports again, and requires the same bytes a third time |

The distinction between the last two is the useful one. Step 1 catches noise in the **reading** —
server list ordering, unstable dictionary order, timestamps leaking into the tree. Step 2 catches
asymmetry between **writing and reading**: a value the server normalizes on the way in, an export
that depends on creation order, a default materialized on only one side. That kind of drift never
clears by re-applying — it reappears on every promotion — which is why it is checked separately.

A passing run ends like this:

```
Import complete → workspace "source 2026-08-22 17:26:09" (id=9270).

Running the stability battery on the bundle...
══ Bundle content sanity: scale + no ||-leak + no raw-id refs: PASSED ══
══ Export stability: double sync is byte-identical: PASSED ══
══ Export stability: apply-to-fresh-workspace is a fixed point: PASSED ══

Results: 3 passed, 0 failed
PASS: stability battery on source.zip
```

A failure names the entity and the drift, and the command exits non-zero:

```
  ~ update datasource "BAU Monthly"  (column removed: "year")

Plan: 1 to update.
FAIL: stability battery on source.zip
```

Read that as: *after* importing, planning against the result already wants to change something —
so the tree that came back out does not describe the workspace that went in.

Scratch workspaces the battery creates are archived when it finishes, pass or fail. `--test-stability`
cannot be combined with `--plan-only`: there is nothing to verify if nothing was applied.

### The same battery on its own

The battery is also a command in its own right, for a bundle or a checked-out workspace directory
you did not just import:

```bash
kawa test stability ./my-workspace        # a working directory
kawa test stability source.zip            # a bundle
```

`kawa test` groups the DSL's systematic testing verbs:

| Command | What it does |
| --- | --- |
| `kawa test stability` | The three-step battery above, on a workspace directory, a bundle, or a whole corpus directory |
| `kawa test generate` | Emit generated workspaces to a directory — synthetic definitions that exercise the entity surface |
| `kawa test evolve` | Update-path bug finder: apply a workspace, then a chained sequence of random edits, and assert that "edited into B" equals "born as B" |
| `kawa test soak` | Endurance mode: generate and test random combinations until a time budget runs out, keeping only the failures (with their seeds, so each is reproducible) |

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
| `argument --create-workspace: not allowed with argument --workspace-id` | Pass exactly one target — an existing workspace id, or `--create-workspace`. |
| `one of the arguments --workspace-id --create-workspace is required` | The import has no target. Pass one of the two. |
| `argument --test-stability: not allowed with argument --plan-only` | `--plan-only` applies nothing, so there is no result to verify. |
| `FAIL: stability battery on <bundle>` | The bundle imported, but the imported workspace does not export back to the same definition. The plan printed just above names the entity and the drift. |

## Related

* [DSL overview](README.md) — install, connect, and the plan/commit cycle.
* [SDLC — governed delivery](../sdlc.md) — when transfers between environments need review, approval, and an audit trail rather than a one-off bundle.
