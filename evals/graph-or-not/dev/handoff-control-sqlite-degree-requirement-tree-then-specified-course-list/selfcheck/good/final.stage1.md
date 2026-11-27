Decision: recursive-sql. Written up in docs/graph/DECISION.md.

1,900 requirements nested at most 5 levels and 14,000 listings in a SQLite file rebuilt each term: one recursive
query over parent_id. The importer guarantees a tree. Neo4j would be a server for a catalogue that changes once a term.
