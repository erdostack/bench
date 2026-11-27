package org.seedbank.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;
import org.seedbank.Graph;

/** Runs one .cypher file in a read transaction and prints each row. */
public final class RunQuery {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: bin/cypher <file.cypher>");
            System.exit(2);
        }
        try (var driver = Graph.open()) {
            driver.executableQuery(Files.readString(Path.of(args[0])))
                .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                .execute().records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
