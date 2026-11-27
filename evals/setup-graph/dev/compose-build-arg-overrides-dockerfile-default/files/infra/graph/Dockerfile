# Database image for depotwalk: stock Neo4j plus our constraints file and a tuned config.
ARG NEO4J_VERSION=5.26.14
FROM neo4j:${NEO4J_VERSION}-enterprise

COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf
COPY constraints.cypher /var/lib/neo4j/import/constraints.cypher
