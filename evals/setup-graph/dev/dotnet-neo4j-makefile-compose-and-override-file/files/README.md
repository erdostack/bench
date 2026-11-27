# ferry-links

Ferry routes between islands and the connections a traveller can make, for the timetable team.
The graph runs on **Neo4j 5.26.24 (LTS)**, the image in `compose.yaml`, started with `make up`.

    make up
    make q F=queries/island_reach.cypher

`make q` runs `tools/FerryQuery`, which opens a read session and prints rows as JSON.
CI starts the same database with `make up` and runs the queries in `queries/` against it.
