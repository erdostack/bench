# Affected tests on PRs

Decision: in-process-library

## Workload (stated 2026-11-23)

- Target graph from the build tool export: about 12k targets, 70k edges; export 20 s; selection gets 30 s more.
- 4,800 test targets; running all of them takes 38 minutes.
- Rule agreed with release: on PRs follow `deps` edges only. Changes reached only through `tools` edges (protoc,
  linters, codegen) are covered by the nightly full run.

## Options

- graph-database (platform offer): rejected; it would be reloaded from the export on every pipeline.
- in-process-library: chosen. Reverse the `deps` edges, walk from the changed targets, keep `kind == "test"`.
- recursive-sql: no SQL database involved.
- no-graph: rejected; the selection is transitive.

## What would change this

- Dropping the deps-only rule (then the affected set is most of the repo and selection buys little).
