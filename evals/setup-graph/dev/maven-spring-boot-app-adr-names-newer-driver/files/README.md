# shelfmark

Inter-library loans: which branch can lend which edition, and the shortest courier chain between two
branches. Spring Boot 3.5 service with Spring Data Neo4j.

- Database: Neo4j, see compose.yaml
- Driver: see ADR 0004 (docs/adr/0004-driver-6.md)
- Ad-hoc queries: `scripts/cypher.sh <file>` (cypher-shell inside the container)
- Schema: db/schema.cypher is applied on start-up
