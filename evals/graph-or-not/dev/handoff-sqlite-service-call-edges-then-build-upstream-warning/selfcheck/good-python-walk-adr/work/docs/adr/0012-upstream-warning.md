# ADR 0012: upstream warning on deploy

Status: accepted

Decision: recursive-sql

The call graph stays in the deploy tool's SQLite file. An edge counts if seen on at least 3 of the last 7 days
(agreed with SRE). 1,400 services, ~31k edges/day, chains to 11 deep, ~230 cycles, so the walk keeps a visited set.
Neo4j (Ines) rejected: a server and a nightly load for one walk.
