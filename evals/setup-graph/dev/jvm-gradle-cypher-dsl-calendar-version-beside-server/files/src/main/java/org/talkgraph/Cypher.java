package org.talkgraph;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** Runs one saved Cypher file as a read query and prints each record. */
public final class Cypher {
    private Cypher() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: Cypher <file.cypher>");
            System.exit(2);
        }
        String query = Files.readString(Path.of(args[0]));
        String uri = System.getenv().getOrDefault("TALKGRAPH_URI", "bolt://localhost:7687");
        String user = System.getenv().getOrDefault("TALKGRAPH_USER", "neo4j");
        String password = System.getenv().getOrDefault("TALKGRAPH_PASSWORD", "");
        try (Driver driver = GraphDatabase.driver(uri, AuthTokens.basic(user, password))) {
            var result = driver.executableQuery(query)
                    .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                    .execute();
            result.records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
