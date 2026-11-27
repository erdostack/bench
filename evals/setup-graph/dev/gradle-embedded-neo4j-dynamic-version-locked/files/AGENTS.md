# For coding agents

- The store in `build/graph-db` is scratch: `./gradlew seed` deletes and rebuilds it from `data/`.
  You may write to it (CREATE, MERGE, SET, DELETE) while developing queries.
- Do not edit `data/` or `gradle.lockfile` by hand.
- Tests: `./gradlew test`.
