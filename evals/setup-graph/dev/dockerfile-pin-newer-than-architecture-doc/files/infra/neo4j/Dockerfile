FROM neo4j:2026.05.0-enterprise

ENV NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    NEO4J_server_memory_heap_max__size=1G

COPY constraints.cypher /var/lib/neo4j/import/constraints.cypher
