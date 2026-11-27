package org.archive.thesaurus;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.dbms.api.DatabaseManagementService;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;
import org.neo4j.graphdb.GraphDatabaseService;

/** Opens the embedded store in var/thesaurus, runs one Cypher file in a transaction that is never committed, prints rows. */
public final class RunCypher {
    private RunCypher() {}

    public static void main(String[] args) throws Exception {
        String query = Files.readString(Path.of(args[0]));
        DatabaseManagementService dbms = new DatabaseManagementServiceBuilder(Path.of("var/thesaurus")).build();
        try {
            GraphDatabaseService db = dbms.database("neo4j");
            try (var tx = db.beginTx(); var result = tx.execute(query)) {
                while (result.hasNext()) {
                    System.out.println(result.next());
                }
                tx.rollback();
            }
        } finally {
            dbms.shutdown();
        }
    }
}
