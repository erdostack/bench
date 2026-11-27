I added `families_within(conn, family, k)` in `seminar/reach.py`.

It runs one recursive SQLite query over `marriage_tie`, following each tie in both directions and stopping after `k` ties. It returns the other families reached, sorted, with the starting family excluded. It returns `[]` when nothing is reachable and for `k = 0` (and for any `k` below 1). A family not in the database also gives `[]`.

Checks: I ran it on a small in-memory graph with `db/schema.sql`, and against a breadth-first search on 200 random graphs for every starting family and k from 0 to 5. All results matched. I did not touch `var/seminar.db`, the app, or `docs/graph/DECISION.md`.
