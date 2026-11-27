# watershed

River network for a catchment: which tributaries drain into which reach, and what lies downstream of a
pollution report. The graph is Neo4j 5.26.24, built from docker/neo4j/Dockerfile.

    make up
    ./gradlew cypher -Pfile=queries/downstream_reaches.cypher
