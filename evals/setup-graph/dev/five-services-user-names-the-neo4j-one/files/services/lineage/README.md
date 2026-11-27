# lineage

Answers "where did this number come from?" for the reporting team: datasets, the jobs that read and write them,
and the report figures at the end of the chain.

## Running it

This service brings its own database; it does not use the shared infrastructure in the repository root.

    docker compose -f dev/compose.yaml up -d
    ./gradlew run
    bin/lq queries/upstream_of.cypher figure=monthly.on_time_rate

`bin/lq` runs one saved query in a read transaction and prints the rows. The graph is filled by the nightly
metadata harvest, which is not in this repository; treat the database as something you read.
