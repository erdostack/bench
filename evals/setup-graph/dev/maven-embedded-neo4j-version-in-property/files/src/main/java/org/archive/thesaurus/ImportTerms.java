package org.archive.thesaurus;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;

/** Loads `label,scheme,broader` rows into the embedded store and commits. */
public final class ImportTerms {
    private ImportTerms() {}

    public static void main(String[] args) throws Exception {
        var dbms = new DatabaseManagementServiceBuilder(Path.of("var/thesaurus")).build();
        try {
            var db = dbms.database("neo4j");
            for (String line : Files.readAllLines(Path.of(args[0])).subList(1, 1)) {
                String[] f = line.split(",");
                db.executeTransactionally(
                        "MERGE (t:Term {label: $l, scheme: $s}) MERGE (b:Term {label: $b, scheme: $s}) MERGE (t)-[:BROADER]->(b)",
                        Map.of("l", f[0], "s", f[1], "b", f[2]));
            }
        } finally {
            dbms.shutdown();
        }
    }
}
