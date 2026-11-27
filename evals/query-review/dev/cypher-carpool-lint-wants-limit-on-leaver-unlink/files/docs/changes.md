# Change files

The release pipeline applies each new file in `db/changes/` once, in file order, with cypher-shell
(auto-commit transactions), against production. A file is never applied a second time.

All environments run Neo4j 5.26. Keep each transaction at or under 5,000 rows.
