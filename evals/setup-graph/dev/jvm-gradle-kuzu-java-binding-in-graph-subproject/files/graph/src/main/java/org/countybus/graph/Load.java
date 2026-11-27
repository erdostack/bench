package org.countybus.graph;

import com.kuzudb.Connection;
import com.kuzudb.Database;
import java.nio.file.Files;
import java.nio.file.Path;

/** Rebuilds var/transfers.kz from data/stops.csv and data/transfers.csv. */
public final class Load {
    public static void main(String[] args) throws Exception {
        Files.createDirectories(Path.of("var"));
        try (Database db = new Database("var/transfers.kz"); Connection conn = new Connection(db)) {
            for (String stmt : Files.readString(Path.of("graph/src/main/resources/schema.cypher")).split(";")) {
                if (!stmt.isBlank()) conn.query(stmt);
            }
            conn.query("COPY Stop FROM 'data/stops.csv' (header = true)");
            conn.query("COPY TRANSFER FROM 'data/transfers.csv' (header = true)");
        }
    }
}
