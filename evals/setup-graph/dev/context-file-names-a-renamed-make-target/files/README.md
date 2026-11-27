# orchard

Records for a heritage orchard: trees, the rootstocks and scions they were grafted from, and which varieties
need which pollination partners nearby.

    export ORCHARD_GRAPH_PASSWORD=<choose one>
    docker compose up -d
    pip install -r requirements.txt
    make query FILE=queries/graft_lineage.cypher

Tooling notes live in `docs/graph/`.
