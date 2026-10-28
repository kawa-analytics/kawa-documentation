# KAWA Train

**KAWA Train** takes what a team builds in one development workspace to production as a sequence of **release trains**. The definition of the workspace lives in a Git repository; a train is a branch of that repository; the host's merge request is the review; a pipeline deploys the merged train onto the controlled environments; and every deploy leaves its proof on a dedicated branch. It is the tooling under the [SDLC](../sdlc.md) model: nothing reaches a governed environment except a committed train, deployed by its version.

## The model in one picture

```
 DEV workspace ──save──▶ train/v1.2.0 ──merge request──▶ master ──deploy v1.2.0──▶ UAT ──▶ PROD
 (everyone builds)       (one train at a time)           (the trunk)               (controlled: nobody edits)
                                                                                      │
                                                            evidence ◀────────── every deploy writes
                                                            (a branch, never merged)   started → finished | failed
```

* **One DEV workspace where everyone builds**, in KAWA, as usual. Nobody works on branches of their own.
* **A train is a branch**, `train/<version>`, cut from the trunk (`master` by default). One train is open at a time. Its commits are *saves*: the whole DEV workspace exported over the tree, with the tickets, the changes by name and the people behind each change in the commit message.
* **The train's record** travels with it: `train/train-<version>.yml` holds its name, description, target date, tickets and members. When the merge request is merged, that file lands on the trunk, and that is what makes the train **merged** — whatever the merge method, with no tag and nobody to remember one.
* **A version deploys from the trunk.** `kawa train deploy prod --ref v1.2.0` finds the trunk commit that carries the train and applies it to the environment, headless, for a pipeline.
* **Every deploy writes its evidence** to the `evidence` branch: a `started` record before the target is touched, a `finished` or `failed` record after. A start with no end holds the environment: two deploys can never run at once.
* **The trunk keeps the history**: its `train/` folder lists every train that shipped; the `evidence` branch says where each one went and when.

## Who does what

| Role | Does | Never |
| --- | --- | --- |
| **Builders** | Build in the DEV workspace | Commit, merge, deploy |
| **Train manager** | Starts the train, names it, puts the tickets and members on it, saves the workspace onto it, opens the merge request — from the page `kawa train` opens | Approve the merge, deploy to a controlled environment |
| **Approver** | Reviews and merges the merge request on the Git host | Build, deploy |
| **Pipeline** | Deploys the merged version onto UAT and PROD with its own service account, and writes the evidence | Edit anything |

Only the DEV key is on a laptop. The keys of the controlled environments live in the pipeline.

## The pages

* [Step-by-step guide](step-by-step.md): from a development workspace to a first train on production, with the output you should see.
* [Reference](reference.md): every verb, the `kawa-flow.yml` file, the train's record, the `.env` file, the evidence branch and the page.
