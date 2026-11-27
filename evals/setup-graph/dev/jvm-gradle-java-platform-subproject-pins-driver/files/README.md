# commitnet

Who-reviews-whom graph built from a generated code-review log: reviewers, authors, files, and the paths between
two people through shared files.

- Neo4j 2026.08.1 (compose.yaml)
- neo4j-java-driver 5.28.1
- Versions for all subprojects live in the `platform` subproject.

Run a query: `./gradlew :query:run --args=queries/review_paths.cypher`
