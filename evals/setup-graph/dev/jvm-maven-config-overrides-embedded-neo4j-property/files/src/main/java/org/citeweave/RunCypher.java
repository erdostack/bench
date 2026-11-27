package org.citeweave;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.dbms.api.DatabaseManagementService;
import org.neo4j.dbms.api.DatabaseManagementServiceBuilder;
import org.neo4j.graphdb.GraphDatabaseService;

/** Opens data/store/ in process and runs one query file in a read transaction that is never committed. */
public final class RunCypher {
    private RunCypher() {}

    public static void main(String[] args) throws Exception {
        String query = Files.readString(Path.of(args[0]));
        DatabaseManagementService dbms = new DatabaseManagementServiceBuilder(Path.of("data/store")).build();
        try {
            GraphDatabaseService db = dbms.database("neo4j");
            try (var tx = db.beginTx()) {
                tx.execute(query).accept(row -> {
                    System.out.println(Json.line(row));
                    return true;
                });
                tx.rollback();
            }
        } finally {
            dbms.shutdown();
        }
    }
}
