# coldchain

Follows vaccine shipments through every hand-off between depots, couriers and clinics, and finds the
hand-offs where the temperature log has a gap.

## The graph

There is no standing database. The integration tests and `bin/q` start a throwaway Neo4j 5.26 LTS
container with Testcontainers (`GraphFixture`, image `neo4j:5.26.24-community`), load
`src/test/resources/fixture.cypher` and run against it:

    bin/q queries/gaps_by_courier.cypher

The service itself talks to the hosted graph through the Neo4j Java driver (`HandoffRepository`).
