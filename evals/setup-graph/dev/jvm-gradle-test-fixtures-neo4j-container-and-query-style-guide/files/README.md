# crewpair

Builds legal crew pairings from flight legs: which legs can follow which at the same airport within
the minimum connection time, and where a pairing can end at the crew base.

## Graph

Tests and ad-hoc queries run against Neo4j 2026.04 in a throwaway Testcontainers container (the
`GraphServer` test fixture). Queries are Cypher 25; see `docs/query-style.md` before writing one.

    bin/q queries/pairings_from_base.cypher

The pairing service reads the hosted graph through the Neo4j Java driver.
