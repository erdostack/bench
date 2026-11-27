package dev.dockyard;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;

final class Graph {
    private Graph() {}

    static Driver open() {
        String password = System.getenv("DOCKYARD_GRAPH_PASSWORD");
        return GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", password));
    }
}
