# Architecture

_Last reviewed: March 2024_

## Graph store

Neo4j 5.18 Enterprise, single instance, built from `infra/neo4j/`. Enterprise is needed for the property
existence constraints on `Pressing`.

## Model

- `(:Release)-[:PRESSED_AS]->(:Pressing)-[:ON_LABEL]->(:Label)`
- `(:Artist)-[:CREDITED_ON {role}]->(:Release)`
- `(:Pressing)-[:REISSUE_OF]->(:Pressing)`
- `(:Label)-[:IMPRINT_OF]->(:Label)`

## Application

A small Node service (`src/`) reads the graph through the official JavaScript driver. There is no write path in
the service; the catalogue is loaded by the shop's stock import, which lives in another repository.
