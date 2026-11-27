# payflow

Money-movement graph for spotting rings of accounts that pass the same funds around.

We run Neo4j 2026.08 (deploy/chart) and write every query in Cypher 25; see docs/query-style.md.

    make deploy forward
    ./gradlew cypher -Pfile=queries/ring_candidates.cypher
