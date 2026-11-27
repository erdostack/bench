# pantry

Recipes, ingredients and substitutions as a graph: which dishes can still be cooked when an ingredient runs out.

- Server: Neo4j 2026.05.0 Community, `docker compose up -d` (compose.yaml)
- Java driver: neo4j-java-driver 6.1.0. pom.xml declares it without a version; the version comes from the
  driver's own BOM, `org.neo4j.driver:neo4j-java-driver-bom`, imported in dependencyManagement.
- Run a saved query: `bin/cypher queries/cookable_without.cypher`
- Constraints and indexes: schema/constraints.cypher
