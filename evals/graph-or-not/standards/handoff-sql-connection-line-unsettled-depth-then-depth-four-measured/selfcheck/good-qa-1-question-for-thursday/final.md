Decision: graph-database

The notes from the first conversation say the line gets 120 ms of the page at 2,400 profile views a second. The
4-step version measured 870 ms p95, about seven times over, and the replica fell 40 s behind while 4,500 new
friendships a second were arriving. Another round of indexes and a bigger instance is a remedy, not a fix for a
seven-fold gap, and our own in-memory graph is ruled out by the 2025-06 incident. Updated notes/connection-line.md
and docs/graph/DECISION.md.
