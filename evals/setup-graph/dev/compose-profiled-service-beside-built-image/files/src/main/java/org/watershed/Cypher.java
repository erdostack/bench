package org.watershed;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** Runs one saved Cypher file against the river network graph, routed as a read, and prints each record. */
public final class Cypher {
    private Cypher() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: Cypher <file.cypher>");
            System.exit(2);
        }
        String query = Files.readString(Path.of(args[0]));
        String uri = System.getenv().getOrDefault("WATERSHED_BOLT", "bolt://localhost:7687");
        String password = System.getenv().getOrDefault("WATERSHED_PASSWORD", "");
        try (Driver driver = GraphDatabase.driver(uri, AuthTokens.basic("neo4j", password))) {
            var result = driver.executableQuery(query)
                    .withParameters(Map.of())
                    .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                    .execute();
            result.records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
