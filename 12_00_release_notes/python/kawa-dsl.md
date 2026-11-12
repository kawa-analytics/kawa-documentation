# kawa-dsl

`kawa-dsl` is the `kawa` command line. It keeps a KAWA workspace as files (TOML definitions, scripts, artifacts) and applies those files to a KAWA server: export, import, plan, commit and the release train.

```
pip install --upgrade kawa-dsl
kawa version
```

The versions are listed newest first. Each one lists what a user of the command line can see; internal changes are left out.

## 2.5.8

**Release date:** 12 November 2026

* **Datasources** — the file of a file datasource is sent to the server in pieces. A large file on a slow connection no longer stops `kawa commit`, `kawa import` or `kawa train deploy` with "The write operation timed out".
* **Import** — every call of an import waits up to 300 seconds for the server, from the first one. The first calls waited 60 seconds, which stopped an import on a slow warehouse. `KAWA_READ_TIMEOUT_SECONDS` sets another value.
* **Sheets** — a lookup column filtered on a column that the same import or commit creates waits for that column. Its filter was left out, and the next plan reported a change.

## 2.5.7

**Release date:** 10 November 2026

**New**

* **Train** — only a KAWA administrator can deploy a train.
* **Train** — a saved train holds the whole workspace, whoever saves it, including what other members built.
* **Sheets** — a computed column is private to its author until its definition says `shared = true`.
* **Agent skills** — a second portable skill, `build-kawa-artifact-lite`, builds a read-only application page (grid, charts, filters) without access to a KAWA server.

**Fixes**

* **Import** — a deploy never copies the deployer's own secret values onto the target.
* **Import** — the artifact and skill versions published on the target are kept as its history.
* **Import** — text such as `NA` stays text when the rows of a bundle are loaded.
* **Export** — a table cut at the 100,000-row limit is reported, never cut silently.
* **Export** — a selective export keeps the file of each script it carries.
* **Sheets** — a declared default view is applied again after an import creates columns.
* **Train** — a save refuses files that the repository's `.gitignore` hides.

## 2.5.6

**Release date:** 5 November 2026

**New**

* **Import** — the rows of a bundle are loaded only into the datasources the import creates. A datasource that already exists on the target keeps its data.
* **Train** — a deploy needs an administrator's key, `--plan` included.
* **Access** — `kawa plan` and `kawa commit` are refused, with a clear message, when the key belongs to a user who cannot build in the workspace.

**Fixes**

* **Commit** — a datasource that reads a computed column not built yet waits for it instead of stopping the commit.

## 2.5.5

**Release date:** 4 November 2026

**New**

* **Live connect** — a live-connect datasource on a table managed by another KAWA workspace is addressed by that workspace's tag, so it follows from one environment to the next.
* **Train** — `kawa train deploy <env> --latest` deploys the last train merged on the trunk.
* **Train** — the trunk is never pushed by the tool, and the prefix of the train branches is configurable (`train_branch_prefix`).
* **Train** — the local page was rebuilt: setup check, connection check, pull, system health, and a light / dark switch.
* **Agent skills** — `build-kawa-artifact` 4.0.0 runs on its own, in one working directory.

**Fixes**

* **Datasources** — on create, the column type written in the definition wins over the type guessed from the data file.
* **Datasources** — two columns whose names differ only by case are kept as two columns.
* **Datasources** — the exported definition records how the server reads a data file.
* **Artifacts** — a workspace works without the large artifact payloads a checkout left on the server.
* **Sheets** — a created lookup column is found by its tag, never by its display name.

## 2.5.3

**Release date:** 2 November 2026

* **Commit** — a datasource written by a workflow and read by a sheet is created before the sheet.
* **Export** — the output datasource of a live workflow is never marked as deleted.
* **Artifacts** — artifact versions download four at a time.

## 2.5.2

**Release date:** 28 October 2026

* **Console** — the output is UTF-8 on every platform, Windows included.

## 2.5.1

**Release date:** 28 October 2026

* **Train** — an environment deploys the commit its predecessor tested: production deploys what UAT tested.

## 2.5.0

**Release date:** 28 October 2026

**New**

* **Train** — `kawa train`, the release train for one shared development workspace, with a local page. See [KAWA Train](../../kawa-flow/README.md).
* **Train** — every deploy records its start and its outcome on a dedicated evidence branch. A deploy that started and never finished holds its environment.
* **Workflows** — two AI tasks: `ai_mapping` (enrich data with AI) and `ai_classify` (decide with AI).
* **Artifacts** — a checkout leaves an artifact payload above 2 MiB on the server, applications excepted.
* **Agent skills** — `build-kawa-artifact` pulls the workspace and publishes the artifact by itself.

**Fixes**

* **Charts** — a sorted chart no longer receives a "top N" limit that its definition does not declare.
* **Apply** — a sheet or a datasource is matched with the server by its tag, never by its display name.
* **Datasources** — the record id of a datasource keeps its tag from one workspace to the next.
* **Commit** — a commit that stops after creating an entity leaves files whose delete works.
* **Train** — a deploy refuses a missing artifact payload before it changes anything.

## 2.4.6

**Release date:** 14 October 2026

**New**

* **Access** — access lives in one file, `dsl/access.toml`: who can read or write each entity, for everyone and per team.
* **Import** — `kawa import --append` adds a bundle to a workspace that holds other content. Only the entities of the bundle are created or updated.
* **Plugins** — `kawa plugin` packages one artifact, the sheets it reads and their editable datasources as an installable zip: `export`, `install`, `list`, `enable`, `disable`.
* **Parameters** — a control-panel parameter is addressed by its immutable tag.
* **Live connect** — a live-connect query addresses datasources by tag: `{{<datasource-tag>}}`.
* **Rollback** — an entity deleted on the target is brought back when the files describe it as live, so a workspace can be rolled back to an earlier version.

**Fixes**

* **Plan** — the plan lists the views deleted with a sheet and the datasources removed with a workflow.
* **Plan** — a deploy that stopped halfway can be run again on the same workspace.
* **Datasources** — a data load that outlives the wait no longer fails the commit; the plan says it is still loading.
* **Datasources** — a column removed from an editable datasource travels with the files.
* **Datasources** — a file re-upload keeps the primary key of a column whose name has an underscore.
* **Workflows** — a failed update leaves the workflow readable.

## 2.4.5

**Release date:** 29 September 2026

**New**

* **Workflows** — `interrupt_workflow` can stop the run in error: `throw_error = true` and `error_message`.
* **Commit** — an apply is up to 4.6 times faster on wide workspaces.
* **Flow** — `kawa flow` opens a local page with the map of environments, a check of each server's key and a first-run wizard. `kawa flow adhoc` deploys any commit into a new workspace.

**Fixes**

* **Export** — an export gives the same text every time, in every process.
* **Sheets** — an edit of an existing lookup is never ignored: a changed measure is applied, a changed target sheet is refused at plan.
* **Filters** — a filter written with keys that KAWA does not read is refused at plan instead of being applied as no filter.
* **Filters** — the aggregation of a date filter survives an import.
* **Datasources** — file timestamps load as UTC by default; the time zone is declared in the definition.
* **Workflows** — an email whose recipient is a variable, a join fed by another join and a sub-process nested in a branch are exported correctly.
* **Logs** — a failed workflow task shows the server's reason.

## 2.4.2, 2.4.3 and 2.4.4

**Release date:** 10 September 2026

**New**

* **Flow** — `kawa flow` promotes a workspace between environments from a Git repository: `init`, `doctor`, `seed`, `feature start`, `pull` and `deploy`.
* **Flow** — the environments are declared in `kawa-flow.yml`, with one API key per environment.
* **Flow** — a datasource can be overridden per environment, for instance as a live connect on production.

**Fixes**

* **Plan** — a name over 255 characters or a description over 1000 characters is refused before anything is applied.
* **Windows** — file writes are retried when an antivirus holds a lock.
* **Sheets** — a half-built sheet is picked up again by the next attempt instead of failing.
* **Workflows** — task ids are always long enough to show in the run history.

## 2.4.0

**Release date:** 6 September 2026

**New**

* **Workflows** — each task carries a stable `task_id`: a renamed task keeps its resources.
* **Scripts** — the pre-flight check warns on every `print()`, because its output is not in the run log.

**Fixes**

* **Connection** — every call to KAWA follows the same TLS settings.
* **Scripts** — registering a script updates the workflows that run it.
* **Artifacts** — the file extension decides the artifact type.
* **Workflows** — a script input column without a mapping is an error, not a silent gap.

## 2.3.0

**Release date:** 28 August 2026

* **Workflows** — `variable_referential`: named constants available to every task.
* **Export** — `--anonymize-data` works on Windows when a file is locked.

## 2.2.0

**Release date:** 27 August 2026

**New**

* **Immutable tags** — columns are addressed by their immutable tag everywhere: datasources, sheets, views, computed columns, dashboards, control panels and workflows. A renamed column keeps its references.
* **Export** — `--no-data` exports the definition only, `--anonymize-data` replaces every value and keeps the column types, `--no-deps` exports exactly the named entities.
* **Import** — `--create-workspace` imports into a new workspace, and `--test-stability` checks that the imported bundle exports to the same definition.
* **Import** — the plan is computed against what the target already holds.
* **Secrets** — a bundle carries the names of the secrets, never their values.
* **Datasources** — primary keys can be changed in place.
* **Agent skills** — portable agent skills, installed with `kawa agent-skill install`.
* **Commit** — a commit ends with one verdict line: `COMMIT OK`, `FAILED`, `CANCELLED` or `PENDING`.

**Fixes**

* **Import** — a second import of the same bundle finds nothing to do: no file is uploaded again, no column is archived twice.
* **Scripts** — scripts and their files are addressed by tag, not by name.
* **Workflows** — a workflow is saved again when a script it runs is registered again.

## 2.1.0

**Release date:** 10 August 2026

**New**

* **Transfer** — `kawa inventory` lists every entity with its tag, `kawa export --tags` exports the named entities with what they depend on, and `kawa import` applies a bundle to another workspace or server.
* **Artifacts and skills** — artifacts and skills are versioned entities of the workspace files.
* **Workflows** — `load_artifact` and `save_artifact` tasks.
* **Scripts** — `kawa scripts register` publishes a script; scripts, artifacts and skills share the same `init`, `register` and `checkout` commands.
* **Sharing** — artifacts and skills carry their access like every other entity.

**Fixes**

* **Commit** — a delete is retried when another user edits the entity at the same time.
* **Filters** — a filter on a boolean column accepts a value of another type.
* **Datasources** — the wait for a data load allows for slow warehouses.
