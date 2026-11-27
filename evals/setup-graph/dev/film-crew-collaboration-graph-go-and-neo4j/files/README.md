# crewgraph

Who worked with whom on the studio's productions: people, productions and credits, for the scheduling
team's "find a crew that has worked together" questions.

Database: Neo4j 5.26.14 Community, the same tag as compose.yaml (bump both together).

    docker compose up -d
    make q F=queries/worked_together.cypher P=pers-0042

Saved queries are read-only. The credits are loaded by `make load` from the production database export.
