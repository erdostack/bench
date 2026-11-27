# citegraph

Citation network for a reading group: which papers cite which, and which ones everyone builds on
without citing.

The graph is Neo4j 2026.05, built from `docker/graph`. All query files are Cypher 25: each one starts
with `CYPHER 25` so that it keeps working when the server's default language changes.

    docker compose up -d --build
    make cypher F=queries/uncited_foundations.cypher
