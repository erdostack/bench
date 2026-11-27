# tidepool

Teaching tool for a marine biology course: the rocky-shore food web as a graph. Who eats whom, and what happens
downstream when a species disappears from a pool.

    export TIDEPOOL_GRAPH_PASSWORD=<choose one>
    npm ci
    npm run db:up
    npm run seed
    npm run cypher -- cypher/top_predators.cypher

`npm run db:up` is `docker compose up -d --wait`; nothing else is needed to get a database.
