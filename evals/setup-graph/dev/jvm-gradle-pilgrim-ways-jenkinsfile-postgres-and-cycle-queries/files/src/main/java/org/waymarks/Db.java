package org.waymarks;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/** Connection from the standard PG* environment variables. */
final class Db {
  static Connection open() throws SQLException {
    String host = System.getenv().getOrDefault("PGHOST", "localhost");
    String port = System.getenv().getOrDefault("PGPORT", "5432");
    String db = System.getenv().getOrDefault("PGDATABASE", "ways");
    String user = System.getenv().getOrDefault("PGUSER", "postgres");
    return DriverManager.getConnection("jdbc:postgresql://" + host + ":" + port + "/" + db, user,
        System.getenv().getOrDefault("PGPASSWORD", ""));
  }
}
