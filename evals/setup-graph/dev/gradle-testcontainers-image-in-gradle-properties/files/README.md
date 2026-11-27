# stagehand

Crew scheduling for a touring theatre company: who can rig which venue, and which shows clash for the
same people. There is no shared database; tests start Neo4j 5.26.25 (the default in GraphFixture)
with Testcontainers and seed it from `src/test/resources/seed.cypher`.

    ./gradlew test
    ./gradlew adhoc -Pcypher=queries/crew_clashes.cypher   # one query against the seeded container
