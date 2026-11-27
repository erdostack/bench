package org.seedbank.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.seedbank.Graph;

/** One-off importer for the paper ledger export (ledger/lots.csv). Run by the librarian, not by tools. */
public final class ImportLedger {
    public static void main(String[] args) throws Exception {
        try (var driver = Graph.open()) {
            for (String line : Files.readAllLines(Path.of("ledger/lots.csv")).stream().skip(1).toList()) {
                String[] f = line.split(",");
                driver.executableQuery("MERGE (v:Variety {name: $variety}) "
                        + "MERGE (l:Lot {code: $code}) SET l.year = toInteger($year) MERGE (l)-[:OF_VARIETY]->(v)")
                    .withParameters(Map.of("code", f[0], "variety", f[1], "year", f[2])).execute();
                if (f.length > 3 && !f[3].isBlank()) {
                    driver.executableQuery("MATCH (c:Lot {code: $code}), (p:Lot {code: $parent}) MERGE (c)-[:GROWN_FROM]->(p)")
                        .withParameters(Map.of("code", f[0], "parent", f[3])).execute();
                }
            }
        }
    }
}
