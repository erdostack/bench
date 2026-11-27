# Migrations

`db/migrations/V<NNNN>__<what>.cypher`, applied once each by the release pipeline as auto-commit
queries. Keep one transaction under about 100,000 changed entities (nodes, relationships or
properties).
