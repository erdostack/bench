package org.countybus.graph;

import com.kuzudb.Connection;
import com.kuzudb.Database;
import com.kuzudb.QueryResult;
import java.nio.file.Files;
import java.nio.file.Path;

/** bin/kq <file.cypher> [stop=S01]: one query against var/transfers.kz, printed as rows. */
public final class Query {
    public static void main(String[] args) throws Exception {
        String cypher = Files.readString(Path.of(args[0]));
        for (int i = 1; i < args.length; i++) {
            String[] kv = args[i].split("=", 2);
            cypher = cypher.replace("$" + kv[0], "'" + kv[1].replace("'", "") + "'");
        }
        try (Database db = new Database("var/transfers.kz"); Connection conn = new Connection(db)) {
            QueryResult result = conn.query(cypher);
            while (result.hasNext()) System.out.println(result.getNext());
        }
    }
}
