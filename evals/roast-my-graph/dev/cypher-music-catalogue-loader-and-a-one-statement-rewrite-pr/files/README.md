# vinylgraph

A catalogue mirror built from a public music metadata dump (identifiers are MBIDs), in Neo4j 5.26.

    load/schema.cypher       constraints
    load/catalogue.cypher    statements, run in file order for every batch
    load/run.py              nightly loader

Sizes: 2.1 million Artist, 4.4 million Release, 5.0 million CREDITED_ON (a release can credit several
artists), 90,000 Label. The loader is one process run nightly on the day's changes; nothing else writes.
