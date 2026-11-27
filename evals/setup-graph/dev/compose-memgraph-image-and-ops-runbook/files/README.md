# gridline

Outage impact for a distribution network: which feeders and customers lose power when a substation or
line trips. The graph runs on Memgraph 2.21 (in memory, snapshot on exit).

    docker compose up -d
    ./gradlew query -Pfile=queries/downstream_of.cypher

Operating notes: docs/ops/runbook.md.
