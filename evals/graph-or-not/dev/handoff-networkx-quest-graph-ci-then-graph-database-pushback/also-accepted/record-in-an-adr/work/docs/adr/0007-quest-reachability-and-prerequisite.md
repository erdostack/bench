# 0007. Quest reachability and prerequisite loops in CI

Status: Accepted
Date: 2026-11-23

Decision: in-process-library

## Workload (stated 2026-11-23)

- About 22k quests, 61k prerequisite edges; YAML under content/quests, changed by about 40 content PRs a day.
- Checks: every quest reachable from a start quest; no cycles in `requires`.
- Prototype: networkx over all the YAML, 1.8 s including parsing, on the CI runners.
- No ops team, nobody on call; CI runners are the only infrastructure.

## Options

- graph-database (Lena): rejected; a server to run and to load from each PR's YAML.
- in-process-library: chosen; networkx in tools/validate.py.
- recursive-sql: no database here.
- no-graph: rejected; both checks are transitive.

## What would change this

- Designers needing an always-on dependency browser: a separate tool, which could read the same YAML.
