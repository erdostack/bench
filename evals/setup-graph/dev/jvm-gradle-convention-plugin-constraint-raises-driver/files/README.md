# stopover

Bird migration stopovers from a generated ringing dataset: which sites are used by the most species, and chains
of sites a flyway passes through.

- Neo4j 2025.10.1 (compose.yaml)
- neo4j-java-driver 5.20.0 (app/build.gradle.kts)
- `./gradlew :app:cypher -Pfile=queries/busiest_sites.cypher`
