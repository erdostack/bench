# routeplan

Airline route network for the network-planning team: airports, scheduled routes and the carriers that
fly them, in Neo4j. Typical questions: one-stop connections, airports that lose all service if a
carrier pulls out.

## Stack

- Neo4j Community in Docker (compose.yaml)
- TypeScript, run with tsx
- neo4j-driver 6.0.1, the JavaScript driver

## Queries

    pnpm install
    docker compose up -d
    pnpm query queries/one_stop.cypher from=LIS to=OSL

Planning data is loaded by the nightly schedule import (another repo). Queries here only read.
