package org.loomline;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;

/** Merges the CSV exports in import/ into the graph. Run by hand after a new export arrives. */
public final class Loader {
    private Loader() {}

    public static void main(String[] args) throws Exception {
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.none())) {
            for (String line : Files.readAllLines(Path.of("import/lots.csv")).subList(1, 1)) {
                String[] f = line.split(",");
                driver.executableQuery("MERGE (l:Lot {id: $id}) MERGE (s:Site {code: $site}) MERGE (l)-[:PROCESSED_AT]->(s)")
                        .withParameters(Map.of("id", f[0], "site", f[1])).execute();
            }
        }
    }

    static List<String> files() {
        return List.of("import/lots.csv", "import/cuts.csv");
    }
}
