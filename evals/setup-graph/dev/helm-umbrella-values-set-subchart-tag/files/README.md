# provenance-atlas

Ownership chains for objects in a museum collection: who held a piece, when, and how it changed hands.
The graph runs in Kubernetes as part of the `atlas` stack: Neo4j 5.26 LTS via the graphdb chart.

    make deploy            # helm dependency build + install deploy/stack
    make forward
    bin/query queries/gaps_in_chain.cypher

