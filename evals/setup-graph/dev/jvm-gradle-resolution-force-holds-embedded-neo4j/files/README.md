# openingbook

Chess opening transpositions: positions are nodes, moves are relationships, so two move orders that reach the
same position meet in one node. The graph lives in an embedded Neo4j 2026.05.0 store in data/book-db/.

    ./gradlew cypher -Pfile=queries/transpositions.cypher
