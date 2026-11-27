# fieldnotes

Bird survey sightings as a graph: `(:Species)-[:SEEN_AT {date, count}]->(:Site)`, for "which species turn
up together" questions. Embedded Kuzu 0.11.1 (the kuzu npm package); the database is `db/survey.kuzu`,
rebuilt by `yarn load` from data/sightings.csv. No server.

    yarn install
    yarn load
    yarn q queries/co_sighted.cypher
