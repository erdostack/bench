# Notes for coding agents

- Java 21. Build with `./gradlew build`; tests need the container from `compose.yaml` to be up.
- Dependency versions are locked in `gradle.lockfile`. Do not edit that file by hand; run
  `./gradlew dependencies --write-locks` if a version has to change, and say so in the PR.
- The Neo4j started by `docker compose up -d` is a disposable development database. It is filled from `fixtures/`
  and holds nothing else. You may run write queries against it (CREATE, MERGE, SET, DELETE); that is what it is
  for. `./gradlew resetGraph` puts it back to the fixture state.
- Never point a tool at a host other than localhost.
- Run a query file with `./gradlew cypher -Pfile=<path to .cypher>`.
