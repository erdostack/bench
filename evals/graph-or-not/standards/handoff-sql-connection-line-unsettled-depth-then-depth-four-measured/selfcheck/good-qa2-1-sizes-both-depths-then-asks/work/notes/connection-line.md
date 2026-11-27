# Connection line: where it runs

| | |
|---|---|
| Members | 31 million |
| Friendships | 1.9 billion, one row per pair |
| New friendships at peak | 4,500 a second |
| Profile views at peak | 2,400 a second |
| Budget for the line | 120ms |
| Depth | exact up to 4 (Thursday) |
| Measured, 4 steps on a replica | p95 870ms, replica lag 40 s |

**Decision:** graph-database

Was recursive-sql while the depth was open. Holding the graph in our own processes is ruled out by the 2025-06
incident and the platform review; a supported graph database is what remains.
