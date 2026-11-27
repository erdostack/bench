# vendorgate

Supplier risk: which of our suppliers depend, through their own suppliers, on the same sub-tier
factory, and how exposed a product line is if one of them stops.

There is no shared database. Integration tests and `bin/q` start a throwaway Neo4j 5.26 container
with Testcontainers and load `src/test/resources/seed.cypher` into it.

    ./mvnw verify                          # unit + integration tests
    bin/q queries/shared_subtier.cypher    # one query against the seeded container
