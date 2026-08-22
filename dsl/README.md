# DSL — your workspace as code

The **KAWA DSL** is a command-line tool that represents a workspace as a set of plain text files. Datasources, sheets, views, dashboards, workflows, scripts, agents, artifacts and skills each become a TOML file on disk. You edit the files, preview the change, and push it back to KAWA — the same way infrastructure-as-code tools manage servers.

It is the tooling layer under [SDLC mode](../sdlc.md): everything a governed pipeline promotes between environments is a DSL tree, and every verb on this page is what CI runs on your behalf. You can also use it on its own, with no pipeline at all — to move a workspace to another server, to review a change before it lands, or to keep a workspace's definition in Git.

## Install

The CLI ships as a Python package and needs Python 3.11 or newer:

```bash
pip install kawa-dsl
kawa --help
```

## Connect

The CLI talks to your KAWA server through two environment variables. Set them in your shell, or drop a `.env` file in the directory you run `kawa` from — it is picked up automatically.

| Variable | Required | Description |
| --- | --- | --- |
| `KAWA_API_URL` | yes | Base URL of your KAWA server, e.g. `https://kawa.mycompany.com`. No trailing slash. |
| `KAWA_API_KEY` | yes | API key from *Settings → API keys*. |
| `KAWA_DSL_HOME` | no | Where local CLI state lives. Defaults to `./.kawa`. |

```bash
kawa status      # branch, workspace, user, connection checks
```

## The working cycle

```bash
mkdir my-workspace && cd my-workspace
kawa init                      # prepare the directory
kawa checkout 12               # download workspace 12 into ./dsl/
# edit the TOML files
kawa plan                      # preview what would change — read-only
kawa commit                    # apply the change to KAWA
```

`kawa checkout` materializes one file per entity:

```
my-workspace/
├── workspace.toml        # which workspace this directory is bound to
├── dsl/
│   ├── datasources/      ├── workflows/
│   ├── sheets/           ├── agents/
│   ├── views/            ├── artifacts/
│   ├── dashboards/       └── skills/
│   └── scripts/          (metadata; sources live below)
├── scripts/              # Python / SQL sources
├── files/                # file-datasource blobs
└── data/                 # editable-datasource rows (exports only)
```

`kawa plan` never writes to the server, and `kawa commit` never deletes an entity unless you explicitly pass `--delete`. Reading before writing is always safe.

## Immutable tags — why a definition is portable

Every entity carries an **immutable tag**: an identity minted once at creation that survives renames and is meaningful on any KAWA server. Cross-references inside the tree resolve through those tags, never through numeric ids.

That is what lets a workspace definition leave the server it was built on. A tree exported from development applies unchanged to staging or production, on the same instance or a different one — the entities are matched by tag, and each environment supplies its own data and its own credentials underneath.

Run `kawa inventory` to list every entity with its tag.

## What you can do

| Area | Commands |
| --- | --- |
| Workspace lifecycle | `kawa init`, `kawa checkout`, `kawa status`, `kawa list` |
| Change management | `kawa plan`, `kawa commit`, `kawa refresh`, `kawa pull`, `kawa check` |
| **Transfer between workspaces and servers** | **`kawa inventory`, `kawa export`, `kawa import`** |
| Governed promotion | `kawa sox snapshot`, `promote`, `deploy`, `drift`, `history` |
| Data, scripts, artifacts | `kawa datasources`, `kawa scripts`, `kawa artifact`, `kawa files` |

Every subcommand documents its own flags: `kawa <command> --help`.

## In this section

* [Export and import](export-and-import.md) — snapshot a workspace into a portable bundle and load it into another workspace, on any server.
