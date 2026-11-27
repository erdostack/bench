Decision: graph-database

SQLite was tuned and still misses (14 min and 3 min 20 s against 10 s on 310M relations), networkx doesn't fit,
and the Neo4j trial hit 2 to 8 s. ADR written: docs/adr/0009-register-links-store.md.
