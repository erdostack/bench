# 1. An embedded graph database instead of a server

Status: accepted

## Context

wordroots is a teaching project. People clone it on a laptop, run two commands and expect a result. Asking them to
start a database server first loses half of them.

## Decision

Use an embedded property-graph database that runs inside the Node process and stores its data in a directory.
We picked LadybugDB: it speaks Cypher, loads CSV files with one statement, and installs as an npm package with
prebuilt binaries for the three platforms our contributors use.

## Consequences

- No container, no ports, no credentials.
- One writer at a time. The loader is the only writer; `pnpm ask` opens the database read-only.
- The database directory is a build artefact. It is rebuilt from `data/` and never committed.

## Follow-up (open)

When this was written the Node binding was published on npm as `lbug`, and that is what `package.json` still
installs. The project has since moved the binding to the `@ladybugdb/core` scope; `lbug` was the early name.
Switching means changing the dependency and the import in `src/store.mjs`. Nobody has done it yet.
