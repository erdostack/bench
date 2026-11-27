Decision: recursive-sql

A rollup down 7 levels of 31,000 BOM lines, 200 times a day, is one recursive query on the SQLite file. A graph
database wouldn't make the references real: SQLite only enforces REFERENCES with PRAGMA foreign_keys = ON on each
connection, and the loader never sets it; fixing the load (or a check for orphans) is what does that. The rollup
follows finance's rule: any missing component anywhere below means no cost, shown as incomplete. Written up in
docs/graph/DECISION.md.
