# KAWA Flow

**KAWA Flow** takes a workspace through environments the way software goes through them: the definition lives in a Git repository, one branch per environment, and a handful of `kawa flow` verbs move it from the development workspace to production. It is the tooling under the [SDLC](../sdlc.md) model — nothing reaches a governed environment except a committed tree, deployed from its branch.

Two pages:

* [Step-by-step guide](step-by-step.md) — from an existing dev workspace to a first production deploy, one command at a time, with the output you should see.
* [Reference](reference.md) — the syntax of every verb, the `kawa-flow.yml` file, and the `.env` file.
