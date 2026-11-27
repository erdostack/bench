# crate-digger

Catalogue browser for a second-hand record shop: releases, pressings, artists and labels, and the reissue chains
between them.

## Stack

- Node 22, pnpm
- Neo4j 5 Enterprise (details in `docs/architecture.md`)

## Getting started

    export GRAPH_PASSWORD=<choose one>
    docker compose up -d --build
    pnpm install
    pnpm cypher cypher/reissue_chain.cypher

`pnpm cypher <file>` runs one saved query and prints the rows.
