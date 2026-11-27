# stacks

Subject browsing for a public library catalogue: works, their editions, and a subject hierarchy where "Beekeeping"
sits under "Animal husbandry" sits under "Agriculture". The interesting queries walk that hierarchy.

## Local development

The catalogue database is not built in this repo. The cataloguing team owns it; every night their server writes a
dump, and we load that dump into a local Neo4j to develop against.

    npm ci
    docker compose up -d
    npm run restore -- dumps/catalogue-latest.dump      # copy the dump into dumps/ first
    npm run cq -- queries/broader_subjects.cypher subject="Beekeeping"

`npm run cq` runs a saved query in a read transaction and prints the rows. The local copy is disposable: restore
again to reset it.
