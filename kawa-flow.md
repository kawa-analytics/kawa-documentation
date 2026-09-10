# KAWA Flow — environments as code

`kawa flow` is the command group that runs the [SDLC](sdlc.md) from a **promotion repository**: a Git repository holding the definition of your workspaces as files. One branch per environment, one file per entity. You describe the environments once in `kawa-flow.yml`, keep the API keys in a git-ignored `.env`, and every verb below reads those two files to know where to connect.

Nothing is implicit. A verb either does exactly what its name says or refuses with a reason — it never switches branches, never commits on your behalf, and never deploys a tree that differs from what is checked out.

## Install

The CLI ships as a Python package (Python 3.11 or newer) and needs `git` on the path:

```bash
pip install kawa-dsl
kawa flow --help
```

## The promotion repository

```
mifid-flow/
├── kawa-flow.yml      # the environments — committed
├── .env               # the API keys — git-ignored, never committed
├── .gitignore         # .env and .kawa/
├── dsl/               # one TOML file per entity (datasources, sheets, views, workflows, …)
├── scripts/           # Python / SQL sources
├── files/             # file-datasource blobs
├── artifacts/         # artifact versions
├── skills/            # skill bundles
└── data/              # editable-datasource rows
```

Each environment owns a Git branch. The tree on a branch *is* the definition of that environment's workspace: `develop` holds what runs in the dev workspace, `master` what runs in production. The tree carries no credentials and no server ids — entities are addressed by their immutable tags — so the same commit deploys unchanged to any environment.

Two modes, detected by the doctor: **remote** when the repository has an `origin` (branches are compared with it before a deploy), **local** when it has none (everything stays in this repository).

## Commands

| Command | What it does |
| --- | --- |
| `kawa flow init` | Bootstraps the repository: `git init`, `kawa-flow.yml` from a template, `.env` placeholder, `.gitignore`, first commit, one branch per environment |
| `kawa flow doctor` | Preflight: is everything in place for the other verbs to work? Exit code 0 when every check passes |
| `kawa flow seed` | Downloads the build workspace into the tree — once, on an empty build branch |
| `kawa flow pull` | Re-exports the workspace behind the checked-out branch over the tree; nothing with Git |
| `kawa flow deploy` | Pushes the checked-out environment branch onto its workspace: plan, confirmation, apply |

Every verb runs from the promotion repository (any directory inside it). `--work-dir <path>` points it elsewhere, before or after the verb:

```bash
kawa flow --work-dir ~/mifid-flow doctor
kawa flow doctor --work-dir ~/mifid-flow
```

A typical first run, from an existing dev workspace to production:

```bash
kawa flow init --name mifid --url https://kawa.acme.com --dev-workspace 771 --prod-workspace 773
# put your key in .env
kawa flow doctor                      # everything green?
kawa flow seed                        # on develop: the dev workspace becomes the tree
git add -A && git commit -m "seed from dev"
git checkout master && git merge develop
kawa flow deploy                      # master → the production workspace
```

### `kawa flow init`

```
kawa flow init [--template dev-prod|dev] [--name FLOW] [--url URL]
               [--dev-workspace N] [--prod-workspace N]
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--template` | `dev-prod` | `dev-prod`: dev → prod on `develop` → `master`. `dev`: a single dev environment |
| `--name` | the directory name | The flow name; it prefixes the workspaces the flow creates |
| `--url` | `https://try.kawa.ai` | The KAWA server of every environment (edit the file for one server per environment) |
| `--dev-workspace` | `1` | The dev workspace id on that server |
| `--prod-workspace` | `2` | The production workspace id on that server |

It refuses to run when a `kawa-flow.yml` already exists, keeps an existing `.env`, and commits only its own two files:

```
$ kawa flow init --name mifid --url https://kawa.acme.com --dev-workspace 771 --prod-workspace 773
kawa flow init — /home/acme/mifid-flow
  ✓ git repository initialized (branch develop)
  ✓ kawa-flow.yml written from template dev-prod — flow 'mifid': dev -> prod (build: dev; branches: develop -> master)
  ✓ .gitignore: .env and .kawa/ ignored
  ✓ .env created — put your key in it: KAWA_API_KEY=kawa-…
  ✓ committed on develop (2bac8b5); branch master created
Next: set the workspace ids in kawa-flow.yml, add your key to .env, then run `kawa flow doctor`.
```

### `kawa flow doctor`

```
kawa flow doctor [--timeout SECONDS]
```

Read-only. It checks, in order: the Git repository; the mode (remote or local); `kawa-flow.yml` (every problem is listed, not just the first); one branch per environment; every URL answers `GET /health` as a KAWA instance (`--timeout`, default 5 seconds each); `.env` holds every key variable in use; the tree is seeded; every override fits its target. Exit code 1 when any check fails, and the last line counts the problems:

```
$ kawa flow doctor
kawa flow doctor — /home/acme/mifid-flow
  ✓ git repository: /home/acme/mifid-flow
  ✓ mode: local — no 'origin' remote, branches are local only (2 branches)
  ✓ kawa-flow.yml: OK — mifid: dev -> prod (build: dev; branches: develop -> master)
  ✓ branch 'develop' exists locally (environment dev)
  ✓ branch 'master' exists locally (environment prod)
  ✓ dev: https://kawa.acme.com is KAWA v1.36.43-g547ff1b1 (application, warehouse, postgres OK)
  ✓ prod: https://kawa.acme.com is KAWA v1.36.43-g547ff1b1 (application, warehouse, postgres OK)
  ✗ .env: KAWA_API_KEY is missing (expected a line KAWA_API_KEY=kawa-…)
  ✗ no source yet (no dsl/ under /home/acme/mifid-flow) — run `kawa flow seed` to export the dev workspace (build environment) into this repository
2 problems
```

### `kawa flow seed`

```
kawa flow seed
```

Starts the build branch from the build environment's live workspace: the workspace is exported — `dsl/`, `scripts/`, `files/`, `artifacts/`, `skills/`, `data/` — over the tree, and the verb stops there. You review the result and commit it yourself.

It runs **once**. It refuses when the build branch already holds a tree (on the branch tip, or on disk), and when the build branch is not the one checked out — seed never switches branches.

```
$ kawa flow seed
kawa flow seed — /home/acme/mifid-flow
  ✓ dev workspace 771 exported from https://kawa.acme.com: 27 entities, files and data included
```

### `kawa flow pull`

```
kawa flow pull
```

The checked-out branch says which workspace: an environment's branch pulls that environment's workspace (`develop` → dev, `master` → prod, per `kawa-flow.yml`). The workspace is exported over the tree, each root replaced whole. That is all — pull does nothing with Git: no check, no commit, no checkout. `git diff` shows what changed on the server since the last commit.

```
$ kawa flow pull
kawa flow pull — /home/acme/mifid-flow
  ✓ prod workspace 773 pulled from https://kawa.acme.com over the tree: 27 entities, files and data included
Next: review with `git status` and `git diff`, then commit on master.
```

### `kawa flow deploy`

```
kawa flow deploy [--yes]
```

Takes no argument: the checked-out branch says which environment receives the tree (`master` → prod). The checkout is the deployment, so it is refused when:

* the branch is not an environment's branch;
* the working tree has uncommitted changes — deploy pushes the committed tree only;
* in remote mode, the branch is behind or ahead of `origin` — what deploys is what was merged;
* the tree holds no entities.

Then the environment's overrides are applied (see [`overrides`](#overrides) below), the plan is computed against the live workspace and shown, and you confirm it. `--yes` skips the question. A declined plan deploys nothing. Files and data travel with the definition.

```
$ kawa flow deploy
…
  ~ update sheet "Trades"  (layouts changed)
  + create workflow "Daily volume report"

Plan: 1 to create, 1 to update.
Apply this plan? [y/N] y
…
kawa flow deploy prod — /home/acme/mifid-flow
  ✓ master checked out at c7fcf12, clean
  ✓ deployed to prod workspace 773 on https://kawa.acme.com: 27 entities (files and data included)
```

Exit code 0 when the plan was applied, 1 otherwise.

## `kawa-flow.yml`

The environment registry, at the root of the promotion repository and committed with it. The environments form a **tree rooted at the build environment**: every other environment names the one it descends from.

```yaml
# kawa-flow.yml
name: mifid                        # the flow name
environments:
  - name: dev
    url: https://kawa-dev.acme.com
    workspace: 771                 # the workspace id on that server
    branch: develop                # the git branch this environment deploys
    build: true                    # exactly one environment carries this flag

  - name: staging
    url: https://kawa-stg.acme.com
    workspace: 772
    branch: staging
    predecessor: dev

  - name: prod
    url: https://kawa.acme.com
    workspace: 773
    branch: master
    predecessor: staging
    api_key: KAWA_PROD_API_KEY     # the .env variable holding this environment's key
    overrides:
      - datasource: orders_ic9mp4gvba   # the tag of a datasource file of the tree
        live_connect: true

  - name: hotfix                   # a second successor of dev: forks are fine
    url: https://kawa-hotfix.acme.com
    workspace: 774
    branch: hotfix
    predecessor: dev
```

### Keys

Top level:

| Key | Required | Meaning |
| --- | --- | --- |
| `name` | yes | The flow name. It prefixes the workspaces the flow creates |
| `environments` | yes | The list of environments, one mapping each |

Per environment:

| Key | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Unique. Letters, digits, `.`, `_`, `-` |
| `url` | yes | The KAWA server, `http(s)://…`, no trailing slash |
| `workspace` | yes | The numeric workspace id on that server |
| `branch` | yes | Unique. The Git branch this environment deploys — flat, no slash (a slash marks a feature branch) |
| `build` | no | `true` on exactly one environment: the root of the tree, the one `kawa flow seed` exports. Defaults to `false` |
| `predecessor` | all but the build one | The environment this one descends from. One predecessor each, any number of successors |
| `api_key` | no | The **name** of the `.env` variable holding this environment's key. Defaults to `KAWA_API_KEY`. Never the key itself |
| `overrides` | no | What a datasource of the tree *is* on this environment — see below |

### Rules

`kawa flow doctor` reports every violation at once:

* the file is a mapping with a non-empty `name` and a list of environment mappings, and nothing else;
* names and branches are unique across environments;
* exactly one environment has `build: true`, and it has no `predecessor`;
* every other environment names a `predecessor` that exists in the file; no cycle, no isolated environment — everything descends from the build one;
* `api_key` is an uppercase variable name (`KAWA_PROD_API_KEY`), never a value starting with `kawa-`.

### Overrides

An override says that a datasource of the tree **is a live connect** on that environment. Nothing else travels — in particular, no query: the tree never sees the real one.

```yaml
    overrides:
      - datasource: orders_ic9mp4gvba
        live_connect: true
```

Three cases at deploy time, all explicit:

| The target… | `kawa flow deploy` |
| --- | --- |
| does not hold that tag in the tree | **Refuses**, before connecting. The doctor names it too |
| lacks the datasource | **Creates** it as a live connect from a placeholder query reproducing the tree's columns, the datasource tag and every column tag imposed. Someone then puts the real query in, on the target, outside the DSL |
| already holds it | **Checks containment**: every column of the tree, by tag, with a compatible type. Compatible → left exactly as it is, data untouched. Not compatible → refused, naming the columns |

The datasource is then left as the target holds it; the rest of the tree deploys around it.

## `.env`

The keys live in a `.env` file at the root of the promotion repository. `kawa flow init` creates the placeholder and git-ignores it; it is never committed, and `kawa-flow.yml` only ever names its variables.

```bash
# Your KAWA API key (Settings → API keys). This file is git-ignored.
KAWA_API_KEY=kawa-0123456789abcdefghijklmnopqrstuvwxyzABCD

# One key per environment when they differ: kawa-flow.yml names the variable
# with `api_key: KAWA_PROD_API_KEY` under that environment.
KAWA_PROD_API_KEY=kawa-ABCDzyxwvutsrqponmlkjihgfedcba9876543210
```

* `KAWA_API_KEY` is the default for every environment that names no `api_key`.
* Every variable an environment names must be present, with a value starting with `kawa-`. The doctor lists each one it expects and which environments use it:

```
  ✓ .env: KAWA_API_KEY present (kawa-…Aina) — dev, staging
  ✓ .env: KAWA_PROD_API_KEY present (kawa-…IZxU) — prod
```
