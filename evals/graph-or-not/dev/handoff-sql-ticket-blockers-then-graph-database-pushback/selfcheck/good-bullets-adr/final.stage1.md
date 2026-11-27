Decision: recursive-sql

Keep src/panels/blockers.sql. ADR: docs/adr/0018-blocked-by-panel.md. The outage came from loops in the data and the
query not guarding against them; that is fixed and the query is 11 ms p95 against 300 ms.
