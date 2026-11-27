# Disruption desk: cut-off stations

Decision: recursive-sql

## Workload facts (from the conversation, 2026-11-24)

- 640 stations, about 9,800 track sections; 120 ms p95; the desk needs an answer within 1 s; about 30 closures
  a day; one box with 8 GB; export rebuilt nightly.

## Options considered

- graph-database (Ravi): rejected. recursive-sql: keep sql/cut_off.sql.

## What would change the decision

- p95 near the 1 s budget.
