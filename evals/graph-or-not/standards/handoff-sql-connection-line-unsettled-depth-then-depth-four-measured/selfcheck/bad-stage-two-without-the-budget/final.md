Decision: graph-database

870 ms p95 is far too slow for anything on a profile page, and 40 s of replica lag means the test was hurting the
replica itself. A graph database is built for this kind of four-step expansion. Wrote docs/graph/DECISION.md.
