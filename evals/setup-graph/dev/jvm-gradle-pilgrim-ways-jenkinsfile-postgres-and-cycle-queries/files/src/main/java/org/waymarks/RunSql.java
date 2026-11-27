package org.waymarks;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

/** RunSql <file.sql>: runs one query read-only and prints rows tab-separated. */
public final class RunSql {
  public static void main(String[] args) throws Exception {
    String sql = Files.readString(Path.of(args[0]));
    try (Connection con = Db.open()) {
      con.setReadOnly(true);
      try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery(sql)) {
        int n = rs.getMetaData().getColumnCount();
        while (rs.next()) {
          StringBuilder line = new StringBuilder();
          for (int c = 1; c <= n; c++) line.append(c > 1 ? "\t" : "").append(rs.getString(c));
          System.out.println(line);
        }
      }
    }
  }
}
