package org.seedbank;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;

public final class Graph {
    private Graph() {}

    public static Driver open() {
        String uri = System.getenv().getOrDefault("SEEDBANK_GRAPH_URI", "bolt://localhost:7687");
        return GraphDatabase.driver(uri, AuthTokens.basic("neo4j", System.getenv("SEEDBANK_GRAPH_PASSWORD")));
    }
}
