# wikilinks

Link structure of a small wiki: orphan pages, link rings, and the shortest click path between two
pages.

The graph is Neo4j 2026.05.0, the default tag in compose.yaml.

    cp .env.example .env      # then set a password in .env
    docker compose up -d
    bin/cypher queries/orphan_pages.cypher
