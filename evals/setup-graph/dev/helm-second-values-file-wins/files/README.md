# pollen

Which orchards share pollinator hives, and how far a disease found in one hive could travel along the
hive moves of a season.

## Running locally

A kind cluster with the graph chart from `deploy/graph`:

    make cluster up forward
    ./gradlew cypher -Pfile=queries/hive_reach.cypher

The version we run is set in deploy/env/base.yaml (Neo4j 2026.05.0).
