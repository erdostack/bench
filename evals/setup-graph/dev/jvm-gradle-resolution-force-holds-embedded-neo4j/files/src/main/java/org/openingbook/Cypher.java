package org.openingbook;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;

/** Runs one query file against data/book-db inside a transaction that is rolled back. */
public final class Cypher {
    private Cypher() {}

    public static void main(String[] args) throws Exception {
        String query = Files.readString(Path.of(args[0]));
        var dbms = new DatabaseManagementServiceBuilder(Path.of("data/book-db")).build();
        try (var tx = dbms.database("neo4j").beginTx()) {
            tx.execute(query).accept(row -> {
                System.out.println(row);
                return true;
            });
            tx.rollback();
        } finally {
            dbms.shutdown();
        }
    }
}
