Still stands: no

The call was no-graph because classes were flat, one class per drug, so a rule matched in one join: 4 ms p95 against
the 200 ms the check gets, on 21k drugs and 140k rules. Nested classes up to 5 levels make it a short walk up the
class tree, which a bounded recursive query on Postgres does; no graph database. I recorded the new call in a
section of README.md.
