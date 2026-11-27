package org.waymarks;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.List;

/** Load: recreates the tables from sql/schema.sql and loads data/waypoints.csv and data/legs.csv. */
public final class Load {
  public static void main(String[] args) throws Exception {
    try (Connection con = Db.open(); Statement st = con.createStatement()) {
      st.execute(Files.readString(Path.of("sql/schema.sql")));
      List<String> wp = Files.readAllLines(Path.of("data/waypoints.csv"));
      try (PreparedStatement ps = con.prepareStatement("INSERT INTO waypoint VALUES (?, ?, ?)")) {
        for (String line : wp.subList(1, wp.size())) {
          String[] p = line.split(",");
          ps.setString(1, p[0]); ps.setString(2, p[1]); ps.setString(3, p[2]); ps.addBatch();
        }
        ps.executeBatch();
      }
      List<String> legs = Files.readAllLines(Path.of("data/legs.csv"));
      try (PreparedStatement ps = con.prepareStatement("INSERT INTO leg VALUES (?, ?, ?)")) {
        for (String line : legs.subList(1, legs.size())) {
          String[] p = line.split(",");
          ps.setString(1, p[0]); ps.setString(2, p[1]); ps.setDouble(3, Double.parseDouble(p[2])); ps.addBatch();
        }
        ps.executeBatch();
      }
    }
  }
}
