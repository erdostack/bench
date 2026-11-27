package org.seedvault.lineage;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** Runs one saved Cypher file against the lineage graph and prints each record. */
public final class Cypher {
    public static void main(String[] args) throws Exception {
        var query = Files.readString(Path.of(args[0]));
        var uri = System.getenv().getOrDefault("LINEAGE_URI", "bolt://localhost:7687");
        try (var driver = GraphDatabase.driver(uri)) {
            var result = driver.executableQuery(query)
                    .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                    .execute();
            result.records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
