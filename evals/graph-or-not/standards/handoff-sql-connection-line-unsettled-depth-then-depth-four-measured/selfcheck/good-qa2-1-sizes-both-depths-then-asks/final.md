Decision: graph-database

The numbers, from notes/connection-line.md and the measurement:

| | |
|---|---|
| p95 of the 4-step query, replayed peak | 870ms |
| What the line gets of the page | 120ms |
| Peak profile views | 2,400 a second |
| Replica lag during the test | 40 s |

That is more than seven times over budget, on a replica that cannot keep up with writes while it runs. Another
round of indexes and a bigger instance is a remedy for a small miss, not this one. Our own in-memory graph is off
the table (platform review), so the line moves to a supported graph database fed from the knows changes, with
Postgres kept as the system of record. notes/connection-line.md and docs/graph/DECISION.md now say graph-database.
