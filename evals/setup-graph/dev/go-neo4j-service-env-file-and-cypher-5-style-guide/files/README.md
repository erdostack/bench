# watershed

Stream reaches, gauges and the dams between them. The service answers "what is downstream of this
spill?" and "which gauges see water from this reach?" over a Neo4j graph.

## Local setup

    cp .env.example .env
    make up
    make q F=queries/downstream_of.cypher ARGS="reach=R-0412"

Query files follow `docs/query-style.md`.
