# ridgeway

Walking routes across the moor, stored as a graph in SQLite: `junction` rows are the nodes, `link` rows
the edges (both directions are walkable). Route finding is a recursive CTE.

The schema's foreign keys keep every link attached to real junctions, so the route queries never have
to check for dangling links.

    ./gradlew build
    bin/sql queries/reachable_within.sql

Design notes: docs/design.md.
