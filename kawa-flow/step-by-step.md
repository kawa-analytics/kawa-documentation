# Step-by-step guide

This guide takes a workspace built in development and deploys it to production, one command at a time. Every step shows the command and the output you should see. The [Reference](reference.md) has the full syntax of each verb and file.

The example: a flow named `mifid`, one KAWA server at `https://kawa.acme.com`, workspace 771 for development and workspace 773 for production.

## Before you start

* Python 3.11 or newer and `git` installed.
* A **dev workspace** that already holds your work — datasources, sheets, views, workflows.
* A **production workspace**, empty. Create it in KAWA and note its id.
* An **API key** (*Settings → API keys*) with access to both workspaces.

```bash
pip install kawa-dsl
kawa flow --help
```

## 1. Create the promotion repository

Pick an empty directory and let `kawa flow init` bootstrap it — Git repository, environment file, key placeholder, one branch per environment:

```bash
mkdir mifid-flow && cd mifid-flow
kawa flow init --name mifid --url https://kawa.acme.com --dev-workspace 771 --prod-workspace 773
```

```
kawa flow init — /home/acme/mifid-flow
  ✓ git repository initialized (branch develop)
  ✓ kawa-flow.yml written from template dev-prod — flow 'mifid': dev -> prod (build: dev; branches: develop -> master)
  ✓ .gitignore: .env and .kawa/ ignored
  ✓ .env created — put your key in it: KAWA_API_KEY=kawa-…
  ✓ committed on develop (2bac8b5); branch master created
Next: set the workspace ids in kawa-flow.yml, add your key to .env, then run `kawa flow doctor`.
```

You are on `develop`, the branch of the dev environment. Open `kawa-flow.yml` — it already describes both environments:

```yaml
name: mifid
environments:
  - name: dev
    url: https://kawa.acme.com
    workspace: 771
    branch: develop
    build: true
  - name: prod
    url: https://kawa.acme.com
    workspace: 773
    branch: master
    predecessor: dev
```

Different servers per environment? Edit the `url` of each one. The file is committed; the keys are not.

## 2. Add your key

Put the API key in `.env`, the git-ignored file `init` created next to `kawa-flow.yml`:

```bash
# .env
KAWA_API_KEY=kawa-0123456789abcdefghijklmnopqrstuvwxyzABCD
```

One key for both environments is enough to start. Production with its own key comes later — see [`api_key`](reference.md#keys) in the reference.

## 3. Check

`kawa flow doctor` is read-only and tells you what is still missing:

```bash
kawa flow doctor
```

```
kawa flow doctor — /home/acme/mifid-flow
  ✓ git repository: /home/acme/mifid-flow
  ✓ mode: local — no 'origin' remote, branches are local only (2 branches)
  ✓ kawa-flow.yml: OK — mifid: dev -> prod (build: dev; branches: develop -> master)
  ✓ branch 'develop' exists locally (environment dev)
  ✓ branch 'master' exists locally (environment prod)
  ✓ dev: https://kawa.acme.com is KAWA v1.36.43-g547ff1b1 (application, warehouse, postgres OK)
  ✓ prod: https://kawa.acme.com is KAWA v1.36.43-g547ff1b1 (application, warehouse, postgres OK)
  ✓ .env: KAWA_API_KEY present (kawa-…ABCD) — dev, prod
  ✗ no source yet (no dsl/ under /home/acme/mifid-flow) — run `kawa flow seed` to export the dev workspace (build environment) into this repository
1 problem
```

One problem left, and the doctor names the next step. Run it any time something looks off: a wrong workspace id, an unreachable server or a missing key all show up here, all at once.

## 4. Seed the tree from the dev workspace

`kawa flow seed` downloads the dev workspace into the repository — every entity as a file, plus scripts, files and data. It runs once, on `develop`, and stops without committing:

```bash
kawa flow seed
```

```
kawa flow seed — /home/acme/mifid-flow
  ✓ dev workspace 771 exported from https://kawa.acme.com: 27 entities, files and data included
```

Look at what arrived, then commit it — this is your first version of the definition:

```bash
git status --short
```

```
?? data/
?? dsl/
?? files/
?? scripts/
```

```bash
git add -A
git commit -m "seed from dev workspace 771"
```

`kawa flow doctor` is all green from here on.

## 5. Keep `develop` in step with the dev workspace

Work goes on in the dev workspace, in KAWA. Whenever you want the branch to reflect it, pull the workspace over the tree — on `develop`, the branch of the dev environment:

```bash
kawa flow pull
```

```
kawa flow pull — /home/acme/mifid-flow
  ✓ dev workspace 771 pulled from https://kawa.acme.com over the tree: 28 entities, files and data included
Next: review with `git status` and `git diff`, then commit on develop.
```

Pull does nothing with Git. `git diff` shows exactly what changed on the server since the last commit — a renamed column, a new view, an edited workflow — and you commit it with a message that says why:

```bash
git status --short
```

```
 M dsl/sheets/trades_8t4od185lw.toml
?? dsl/views/by-counterparty_zyolx839rg.toml
```

```bash
git add -A
git commit -m "MIFID-123: volume by counterparty view"
```

## 6. Optional: production reads its own data

A datasource that loads data through a script in development is often a **live connect** to the warehouse in production. Say so in `kawa-flow.yml`, under the production environment — the datasource is named by its tag, found at the top of its file under `dsl/datasources/`:

```yaml
  - name: prod
    url: https://kawa.acme.com
    workspace: 773
    branch: master
    predecessor: dev
    overrides:
      - datasource: trades_ic9mp4gvba
        live_connect: true
```

```bash
git commit -am "prod: Trades is a live connect"
```

No query goes in the file. On the first deploy the datasource is created in production as a live connect from a placeholder query, with the tree's column tags; you then put the real query in, in KAWA, on the production workspace. Later deploys check that it still serves every column the tree expects and leave it alone. The three cases are in the [reference](reference.md#overrides).

## 7. Deploy to production

Production deploys from `master`. Bring `develop` into it, then deploy — the checked-out branch says which environment receives the tree, so there is nothing to type:

```bash
git checkout master
git merge develop
kawa flow deploy
```

The plan is computed against the live production workspace and shown before anything is written. The first time, everything is a create:

```
datasource "Trades" (trades_ic9mp4gvba) is bound to the target by an override — left as the target holds it

  + create script "load_trades"
  + create sheet "Trades"
  + create sheet "Counterparties"
  + create workflow "Daily volume report"
  …

Plan: 27 to create.
Apply this plan? [y/N] y
…
kawa flow deploy prod — /home/acme/mifid-flow
  ✓ master checked out at 9f3e2a1, clean
  ✓ override trades_ic9mp4gvba: not on the target — live connect "Trades" created from a placeholder query (12 column tags imposed); put the real query in on the target
  ✓ deployed to prod workspace 773 on https://kawa.acme.com: 28 entities (files and data included)
```

Answer `n` and nothing is deployed. `kawa flow deploy --yes` skips the question — for a CI job, once you trust the plan.

Deploy refuses to guess: uncommitted changes, a branch that is not an environment's, or (with a Git remote) a branch that differs from `origin`, each stop it with a message saying what to do.

## 8. The next change

From here on, every change follows the same loop:

```bash
git checkout develop
kawa flow pull                  # the dev workspace → the tree
git add -A && git commit -m "MIFID-124: settlement date on trades"

git checkout master
git merge develop
kawa flow deploy                # the tree → the production workspace
```

The plan on the second deploy lists only what changed:

```
  ~ update datasource "Trades"  (column added: "settlement_date")

Plan: 1 to update.
Apply this plan? [y/N] y
```

## 9. Optional: share the repository

Push the repository to your Git server and the flow switches to **remote** mode: the doctor reports it, and `kawa flow deploy` checks that the branch matches `origin` before deploying — what deploys is what was merged and reviewed there.

```bash
git remote add origin git@gitlab.acme.com:acme/mifid-flow.git
git push -u origin --all
kawa flow doctor
```

```
  ✓ mode: remote — origin git@gitlab.acme.com:acme/mifid-flow.git reachable (2 branches)
```

From then on, `git pull` before a deploy and `git push` after a commit, as with any shared repository.
