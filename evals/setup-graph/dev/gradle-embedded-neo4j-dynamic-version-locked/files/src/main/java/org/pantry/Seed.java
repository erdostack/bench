package org.pantry;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;

/** Deletes build/graph-db and loads data/substitutions.csv into a fresh store. */
public final class Seed {
    private Seed() {}

    public static void main(String[] args) throws Exception {
        Path store = Path.of("build/graph-db");
        if (Files.exists(store)) {
            try (var walk = Files.walk(store)) {
                walk.sorted(java.util.Comparator.reverseOrder()).forEach(p -> p.toFile().delete());
            }
        }
        var dbms = new DatabaseManagementServiceBuilder(store).build();
        try {
            var db = dbms.database("neo4j");
            for (String line : Files.readAllLines(Path.of("data/substitutions.csv")).subList(1, 4)) {
                String[] f = line.split(",");
                db.executeTransactionally(
                        "MERGE (a:Ingredient {name: $a}) MERGE (b:Ingredient {name: $b}) MERGE (a)-[:REPLACED_BY {diet: $d}]->(b)",
                        Map.of("a", f[0], "b", f[1], "d", f[2]));
            }
        } finally {
            dbms.shutdown();
        }
    }
}
