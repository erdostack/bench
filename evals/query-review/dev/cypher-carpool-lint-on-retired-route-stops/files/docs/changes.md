# Change files

The release pipeline applies each new file in `db/changes/` once, in file order, with cypher-shell
(auto-commit transactions), against production. All environments run Neo4j 5.26.

Keep each transaction at or under 10,000 rows.
