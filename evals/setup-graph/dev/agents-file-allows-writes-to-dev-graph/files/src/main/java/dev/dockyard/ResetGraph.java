package dev.dockyard;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

/** Deletes everything in the dev database, then loads fixtures/ports.csv and fixtures/voyages.csv. */
public final class ResetGraph {
    public static void main(String[] args) throws Exception {
        try (var driver = Graph.open()) {
            driver.executableQuery("MATCH (n) DETACH DELETE n").execute();
            for (String line : Files.readAllLines(Path.of("fixtures/ports.csv")).subList(1, 5)) {
                String[] f = line.split(",");
                driver.executableQuery("MERGE (:Port {code: $code, berths: $berths})")
                    .withParameters(Map.of("code", f[0], "berths", Integer.parseInt(f[1]))).execute();
            }
            for (String line : Files.readAllLines(Path.of("fixtures/voyages.csv")).stream().skip(1).toList()) {
                String[] f = line.split(",");
                driver.executableQuery(
                        "MATCH (a:Port {code: $from}), (b:Port {code: $to}) "
                        + "MERGE (s:Ship {name: $ship}) "
                        + "CREATE (s)-[:SAILS {departs: date($departs)}]->(v:Voyage)-[:FROM]->(a), (v)-[:TO]->(b)")
                    .withParameters(Map.of("ship", f[0], "from", f[1], "to", f[2], "departs", f[3])).execute();
            }
        }
    }
}
