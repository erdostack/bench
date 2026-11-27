# Shutdown check

Decision: in-process-library

## Workload facts

- 640 stations, 1,500 segments, changes a few times a year; about 30 checks a day.

## Options considered

- graph-database: rejected. in-process-library: chosen. recursive-sql: possible. no-graph: no.

## What would change the decision

- Live checks across all halls.
