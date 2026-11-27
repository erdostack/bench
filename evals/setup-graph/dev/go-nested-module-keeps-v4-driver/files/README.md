# foodweb

Predator-prey links of a generated lake ecosystem: trophic levels, and which species a collapse would cascade to.

## Setup

- Neo4j 5.26.24 Community (compose.yaml)
- Driver: neo4j-go-driver 4.4
- Constraints: schema/constraints.cypher

## Queries

    make q F=queries/cascade.cypher
