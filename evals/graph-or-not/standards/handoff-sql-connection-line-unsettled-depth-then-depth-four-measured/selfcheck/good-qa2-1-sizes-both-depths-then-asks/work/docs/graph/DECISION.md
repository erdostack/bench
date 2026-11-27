# Connection line

Decision: graph-database

Depth settled on Thursday: exact up to 4. The 4-step query on a replica: p95 870 ms against the 120 ms the line
gets, at 2,400 views a second; replica lag 40 s. Details and the earlier call (recursive-sql while the depth was
open) in notes/connection-line.md.
