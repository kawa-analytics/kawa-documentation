# Reference

`kawa train` is the command group of the release train; `kawa flow` keeps the verbs that set a repository up. Both read two files at the root of the repository: `kawa-flow.yml`, committed, describes the environments; `.env`, git-ignored, holds the key.

Nothing is implicit. A verb either does exactly what its name says or refuses with a reason on `stderr` and exit code 1. No verb merges on the host, and no verb deploys a tree that is not a committed train.

## Install

```bash
pip install kawa-dsl
kawa train --help
```

Python 3.11 or newer, `git` on the path.

## The repository

```
mifid/
├── kawa-flow.yml                 # the environments — committed on the trunk
├── .env                          # KAWA_API_KEY — git-ignored, never committed
├── .gitignore                    # .env and .kawa/
├── train/
│   └── train-v1.0.0.yml          # one record per train; the trunk keeps every shipped one
├── dsl/                          # one TOML file per entity (datasources, sheets, views, workflows, …)
├── scripts/                      # Python / SQL sources
├── files/                        # file-datasource blobs
├── artifacts/                    # artifact versions
├── skills/                       # skill bundles
└── data/                         # editable-datasource rows
```

Three kinds of branches, on `origin`:

| Branch | Holds | Who writes |
| --- | --- | --- |
| `master` (the **trunk**; `trunk:` in `kawa-flow.yml` names another) | What shipped: the merged trains, and their records under `train/` | The host, at each merge |
| `train/<version>` | One open train: its record, then its saves | `kawa train start` and `kawa train save` |
| `evidence` | One record per deploy, started → finished or failed. An orphan: no history in common with the trunk, never merged | `kawa train deploy` |

A remote is mandatory: every save is pushed, and the merge only means something on the shared repository. The verbs read branches on `origin`, never from the local clone alone.

## The verbs

| Command | What it does |
| --- | --- |
| `kawa train` | Opens the page in your browser |
| `kawa train start <version>` | Cuts `train/<version>` from the trunk's tip on origin and pushes it with its record |
| `kawa train status [--json]` | The train from git: open or merged, its saves, the shipped trains and where they are deployed |
| `kawa train tickets [add\|remove\|clear …]` | The tickets on the open train |
| `kawa train save [-m "…"]` | The DEV workspace becomes the next commit of the train, pushed |
| `kawa train deploy <env> --ref <version> --yes\|--plan` | A merged train onto an environment, headless; its evidence written |
| `kawa train close <env> [-m "…"]` | Ends a deploy that started and never ended, with a failed record |
| `kawa flow init`, `kawa flow origin <url>`, `kawa flow doctor` | Set the repository up from a terminal: the registry, the remote, the checks |

Every verb runs from the repository (any directory inside it). `--work-dir <path>` points it elsewhere.

### `kawa train`

```
kawa train [--port N] [--no-open]
```

Starts a local server bound to `127.0.0.1` and opens the page. The URL carries a token; only that URL reaches the server. The page is the train manager's: it runs the verbs below and shows their output. See [the page](#the-page).

### `kawa train start`

```
kawa train start <version>
```

Cuts `train/<version>` from `origin/<trunk>`, writes `train/train-<version>.yml` with the version, commits it as `kawa train: start <version>` and pushes the branch. The version is yours to choose: letters, digits, `.`, `-`, `_`, forty characters at most; it names the branch and the record.

Refused when: the repository has no remote; the working tree has uncommitted changes (an unsaved edit of a merged train's record is dropped instead, and said); the trunk already holds `train/train-<version>.yml` (that version shipped); the branch exists; another train is open. One train at a time.

```
$ kawa train start v1.0.0
train/v1.0.0 cut from origin/master, checked out and pushed (593a06e) — name it, put the tickets on it, save
```

### `kawa train save`

```
kawa train save [-m "note"]
```

On the open train's branch: pulls it from origin (fast-forward only), exports the DEV workspace over the tree, files and data included, and commits what differs, pushed. The record rides along. Refused when another branch is checked out, when the working tree has changes other than the record, or when the branch has diverged from origin.

The commit message:

```
the Q3 cut                                      ← the note, when given: the title git shows

kawa train save: 3 changes (KAWA-123, KAWA-130) ← the machine line: the count and the tickets

Train: November release (v1.0.0, target 2026-11-15)
The wines X-Ray dashboard for the trading desk.

Tickets:
  KAWA-123
  KAWA-130

Members:
  Alice Smith
  Bob Lee

Changes:
  + sheet "Trades"  dsl/sheets/trades_8t4od185lw.toml
  ~ view "By counterparty"  dsl/views/by-counterparty_zyolx839rg.toml
  - workflow "Old report"  dsl/workflows/old-report_k2m9x1pq0r.toml

People (owners of what changed):
  Alice Smith — sheet "Trades", view "By counterparty"
  Bob Lee — workflow "Old report"
```

Without a note, the machine line is the title. A record edit with no workspace change is saved as `kawa train save: record updated (…)`. Nothing to save, nothing committed.

```
$ kawa train save -m "the Q3 cut"
kawa train save — /home/acme/mifid
  ✓ train/v1.0.0 pulled from origin
  ✓ dev workspace 771 pulled from https://kawa.acme.com over the tree: 27 entities, files and data included
  ✓ saved on train/v1.0.0 (eb234ab): 3 changes, 2 tickets and pushed
```

The *Analyse changes* button of the page is the same export, over a copy of the train's tip, with nothing committed: it reports what a save would carry.

### `kawa train status`

```
kawa train status [--json]
```

Reads git only, from the last fetch (the page fetches first). The open train and its status, **merged** with the date and the trunk commit, or **not merged**; its saves with their notes; the tickets; the merge request link while it is open; the shipped trains; and, from the evidence branch, where each one is deployed and which version each environment runs.

```
$ kawa train status
kawa train status — /home/acme/mifid
mifid: dev -> prod · remote mode · origin git@gitlab.com:acme/mifid.git
train: train/v1.1.0 → master · not merged
name: December release · target 2026-12-10
tickets: KAWA-140
  7f734cd  Chang the train name  (emmanuel, 2026-10-28)
  593a06e  kawa train: start v1.1.0  (emmanuel, 2026-10-28)
merge request: https://gitlab.com/acme/mifid/-/merge_requests/new?…
shipped on master: v1.0.0 (2026-10-27)
```

### `kawa train tickets`

```
kawa train tickets                     # list
kawa train tickets add KAWA-123 KAWA-130
kawa train tickets remove KAWA-130
kawa train tickets clear
```

Edits the open train's record, as the page does. A ticket key is letters, digits, `-`, `_`, `.`, forty characters at most. Refused with no open train, and on a merged train: its record is read-only.

### `kawa train deploy`

```
kawa train deploy <env> --ref <version|commit|branch> (--yes | --plan)
                        [--skip-large] [--delete] [--json]
```

What a pipeline calls. It runs from a clone of the repository, any branch checked out, and never moves the checkout. In order:

1. **Preflight.** `<env>` is an environment of `kawa-flow.yml` and not the build one. `--yes` or `--plan`, one of the two: there is no prompt. `KAWA_API_KEY` holds the environment's key. The evidence branch is fetched: a `started` record with no end on `<env>` refuses the deploy.
2. **The commit.** Origin is fetched. A version resolves to the last commit on the trunk's first-parent line that touched `train/train-<version>.yml`: the merge commit, the squash commit, or the train's last save after a fast-forward or a rebase. Otherwise `--ref` is a commit or a branch, as git resolves it.
   **The chain.** When `<env>` follows another controlled environment in `kawa-flow.yml` (prod after uat), a version deploys the commit that environment's evidence recorded for it, so what was tested is what goes live. It is refused when the predecessor has no applied deploy of the version (*deploy uat first*), and when the trunk's lookup now names another commit than the one tested. A sha or a branch as `--ref` skips the chain.
3. **The tree**, read in a throwaway worktree. An artifact version whose payload is not in the tree refuses the deploy, every one named, unless `--skip-large`: each such artifact is then deployed up to its last version in the tree and the report says so.
4. **The evidence**: a `started` record, pushed, before anything is touched. No record, no deploy.
5. **The apply.** The environment's overrides are applied, then the tree goes through the import: the plan, then with `--yes` the apply, files and data included. A deletion, an entity the target holds that the train does not declare, blocks unless `--delete`. A 412 "updated by another user" from the server runs the import again from where it stopped, twice at most.
6. **The evidence**: a `finished` record with the result, or a `failed` record with the error. `--json` prints that record.

```
$ kawa train deploy prod --ref v1.0.0 --yes --delete
kawa train deploy prod v1.0.0 — /builds/acme/mifid
  ✓ v1.0.0 at 7e51101: 27 entities
  ✓ evidence: prod/20261028T091402.512033Z-v1.0.0-started.json (3f2a1c0)
  ✓ deletions allowed: what the train does not declare is removed from prod
  ✓ deployed onto prod workspace 773 on https://kawa.acme.com (files and data included)
  ✓ evidence: prod/20261028T091530.004811Z-v1.0.0-finished.json (a2b9c47)
```

Exit code 0 when the plan was applied (or shown, with `--plan`), 1 otherwise.

The job needs the whole history of the repository (GitLab: `GIT_DEPTH: 0`; GitHub Actions: `fetch-depth: 0`; Bitbucket: `clone: depth: full`), read access to origin, and push rights on the `evidence` branch for its identity.

### `kawa train close`

```
kawa train close <env> [-m "why"]
```

A deploy that started and never wrote its end, because its job was killed or its machine went down, holds the environment. `close` writes a `failed` record, `closed by hand: <why>`, with the identity of whoever runs it, and the next deploy can run. Refused when the environment's last record is not a start.

### `kawa flow init`, `kawa flow origin`, `kawa flow doctor`

The setup verbs, for a terminal; the page's setup screen does the same.

| Command | What it does |
| --- | --- |
| `kawa flow init [--name …] [--url …] [--dev-workspace N] [--prod-workspace N]` | `git init`, `kawa-flow.yml`, a `.env` placeholder, `.gitignore`, the first commit. Edit the file to the shape below afterwards |
| `kawa flow origin <url>` | Adds the remote and pushes the trunk |
| `kawa flow doctor [--timeout S]` | Read-only. The repository, the remote, `kawa-flow.yml`, the branches, every server, the key, the tree, the overrides, the open train. Exit code 1 when any check fails |

```
$ kawa flow doctor
kawa flow doctor — /home/acme/mifid
  ✓ git repository: /home/acme/mifid
  ✓ mode: remote — origin git@gitlab.com:acme/mifid.git answers (3 branches)
  ✓ kawa-flow.yml: OK — mifid: dev -> prod
  ✓ dev: https://kawa.acme.com is KAWA v1.37.2 — KAWA_API_KEY accepted (alice@acme.com)
  ✓ prod: https://kawa.acme.com is KAWA v1.37.2 — key not tested here: the pipeline sets KAWA_API_KEY when it deploys
  ✓ .env: KAWA_API_KEY present (kawa-…ABCD)
  ✓ source: dsl/ present (27 entity files)
  ✓ train: train/v1.0.0 open (version v1.0.0, merges onto master)
```

#### Setting up from the terminal

```bash
mkdir mifid && cd mifid
kawa flow init --name mifid --url https://kawa.acme.com --dev-workspace 771 --prod-workspace 773
# edit kawa-flow.yml to the shape below; put the DEV key in .env
git add kawa-flow.yml && git commit -m "the flow"
kawa flow origin git@gitlab.com:acme/mifid.git
kawa flow doctor
```

## `kawa-flow.yml`

The environments, at the root of the repository and committed on the trunk. In the order of promotion: the build one, then each controlled one.

```yaml
# kawa-flow.yml
name: mifid                        # free text; the merge request title starts from the train's own name
host: gitlab                       # optional: gitlab, github, bitbucket-cloud, bitbucket-server —
                                   # needed for a self-hosted server, not for the public ones
trunk: master                      # optional: the branch the trains merge onto; master by default

environments:
  - name: dev
    url: https://kawa-dev.acme.com
    workspace: 771
    build: true                    # exactly one: the DEV workspace where everyone builds

  - name: uat
    url: https://kawa-uat.acme.com
    workspace: 802
    controlled: true               # deploy-only: nobody edits, the pipeline deploys

  - name: prod
    url: https://kawa.acme.com
    workspace: 773
    controlled: true
    overrides:                     # optional: what a datasource of the tree IS on this environment
      - datasource: trades_8zon57i03n
        live_connect: true
```

### Keys

Top level:

| Key | Required | Meaning |
| --- | --- | --- |
| `name` | yes | The flow's name |
| `environments` | yes | The list of environments, one mapping each |
| `host` | no | The Git host family behind `origin`, for the merge request link: `gitlab`, `github`, `bitbucket-cloud`, `bitbucket-server`. The public hosts are recognised from the URL |
| `trunk` | no | The branch the trains merge onto. `master` by default |

Per environment:

| Key | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Unique. Letters, digits, `.`, `_`, `-` |
| `url` | yes | The KAWA server, `http(s)://…`, no trailing slash |
| `workspace` | yes | The numeric workspace id on that server |
| `build` | one environment | `true` on the DEV workspace: the one the trains save |
| `controlled` | no | `true` on a deploy-only environment |
| `api_key` | no | The **name** of the `.env` variable holding this environment's key, when it is not `KAWA_API_KEY`. Never the key itself |
| `overrides` | no | Per datasource, what it is on this environment: see below |

`branch` and `predecessor` are accepted for an environment that deploys a branch other than the trunk, or an order of promotion other than the list's; a train needs neither.

### Overrides

An override says that a datasource of the tree **is a live connect** on that environment. Nothing else travels, in particular no query: the tree never sees the real one. The datasource is named by its tag, found at the top of its file under `dsl/datasources/`.

| The target… | `kawa train deploy` |
| --- | --- |
| does not hold that tag in the tree | **Refuses**, before connecting. The doctor names it too |
| lacks the datasource | **Creates** it as a live connect from a placeholder query reproducing the tree's columns, the datasource tag and every column tag imposed. Someone then puts the real query in, on the target, in KAWA |
| already holds it | **Checks containment**: every column of the tree, by tag, with a compatible type. Compatible: left exactly as it is, data untouched. Not compatible: refused, naming the columns |

## `train/train-<version>.yml`

The train's record, written by `kawa train start` on the train's branch and edited by the page; the merge carries it onto the trunk, which keeps one file per shipped train.

```yaml
name: November release              # the merge request's title
description: |                      # what it delivers, in business words
  The wines X-Ray dashboard for the trading desk.
version: v1.0.0                     # the branch train/v1.0.0 and this file's name
target_date: 2026-11-15             # when it should be live
tickets:
  - KAWA-123
  - KAWA-130
members:                            # the people on the train, picked among the workspace's members
  - Alice Smith
  - Bob Lee
saved_at: 2026-10-27T18:31:02+00:00 # stamped by every save
```

Every field but the version is optional. `saved_at` is what lets a version be found on the trunk whatever the merge method: the last trunk commit that touched the file is the train.

A train is **merged** when `origin/<trunk>` holds its file. From then on the record is read-only, on the page and for the verbs.

## `.env`

One variable, `KAWA_API_KEY`, at the root of the repository, git-ignored:

```bash
# Your KAWA API key (Settings → API keys). This file is git-ignored.
KAWA_API_KEY=kawa-0123456789abcdefghijklmnopqrstuvwxyzABCD
```

Whoever runs a command sets it to the key of the environment that command talks to: on the train manager's laptop the DEV key, in a pipeline job the key of the environment the job deploys to, as a protected variable. No laptop holds a production key. An environment whose key must come from another variable names it with `api_key`.

## The evidence branch

`evidence` is an orphan branch, created by the first deploy, never merged. Each deploy appends records under `<environment>/`, one commit each, named by a UTC timestamp, the version and the kind:

```
prod/20261028T091402.512033Z-v1.0.0-started.json
prod/20261028T091530.004811Z-v1.0.0-finished.json
```

| Kind | Written | Holds |
| --- | --- | --- |
| `started` | Once the target answers, before anything is applied | Environment, workspace, URL, version, commit and tree hash, who (git identity and the key's KAWA principal), host, the pipeline's own identifiers when a host sets them, the flags |
| `finished` | After the apply | The same, plus the result, the 412 retries, what `--skip-large` left out, whether deletions were allowed, the steps |
| `failed` | After a failure, or by `kawa train close` | The same, plus the error and the step |

The rules it enforces:

* **No record, no deploy.** A `started` record that cannot be pushed refuses the deploy and leaves nothing behind.
* **A start with no end holds the environment.** The next deploy refuses, naming the version, the time and the person, until a `finished` or `failed` record follows. Two deploys starting together are settled by the push: one lands, the other reads the branch again and stops.
* **A closing record that cannot be pushed** stays committed locally and the report says *NOT PUSHED*, with the command to push it; the target is already deployed.
* **A push that does not answer within 90 seconds** is killed and retried once on a fresh connection.

What makes the branch impartial is your host: protect `evidence` so that only the pipeline's identity can push to it and nobody can force-push. People read it; a deploy run from a laptop writes with that person's identity, which the weekly reconciliation then sees.

`kawa train status` and the page read the branch back: per environment the deploys that applied, newest first; per train the environments it is on, since when, and whether it is what the environment runs now.

## The page

`kawa train` serves one page, on `127.0.0.1`, with a token in its URL. Two screens on the rail:

**Train.** With no open train: *Start a train*. With one: its name as the title, the branch, **merged** with the date or **not merged**, the remote, the chips of the environments it is deployed on; the record as a property list, read-only once merged; *Analyse changes* and *Save*, with a Saved or Save failed label and its details; the saves embedded in the train, each opening on what it changed; the previous trains with their merge dates and deployments. *Create merge request* while the train is open; *Start the next train* once it is merged.

**Set up the flow.** The configuration editor with examples and a help guide, the DEV key, the repository, and a line that says when the flow is ready. The doctor runs when its dot on the rail is opened.

The page runs the verbs above and nothing else: it holds no state of its own, and everything it shows is in git.
