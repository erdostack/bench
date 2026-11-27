# Contributing to curio

## Environment

We use Poetry. `make install` creates the virtualenv from `poetry.lock`; please do not install with pip, the
resolver picks different versions and the CI image will not match your machine.

    make install
    make up
    make test

## Queries

- Saved queries live in `queries/`, one file per question, parameters as `$name`.
- Run one with `make query Q=queries/<file>.cypher`.
- Anything under `queries/drafts/` is not used by the application. Drafts are written for the server we plan to
  move to (see `docs/upgrade-plan.md`) and start with `CYPHER 25`; they do not run on the current server.
- New queries should avoid syntax that Cypher 25 removes, so the move is cheap when it comes.

## Data

`make load` is for maintainers refreshing the shared development database from the registrar's export. If you are
not sure whether you are a maintainer for this purpose, you are not.

## Reviews

One approval. Query changes need a second pair of eyes from someone who has read `docs/graph-model/overview.md`.
