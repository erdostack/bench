Decision: recursive-sql

A rollup of 23,000 people over about 1,900 units at most 8 levels deep, once a month: one WITH RECURSIVE query
on the unitbook file (each unit joined to all its descendants, then summed) runs in well under a second. A graph
database would be a second store to keep in sync for a monthly report. Noted in docs/graph/DECISION.md.
