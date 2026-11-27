package org.example.corridors;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.Properties;

/** Runs one SQL file against data/corridors.db, read-only, and prints tab-separated rows. */
public final class Sql {
    public static void main(String[] args) throws Exception {
        String sql = Files.readString(Path.of(args[0]));
        Properties props = new Properties();
        props.setProperty("open_mode", "1"); // SQLITE_OPEN_READONLY
        try (Connection c = DriverManager.getConnection("jdbc:sqlite:data/corridors.db", props);
             PreparedStatement st = c.prepareStatement(sql)) {
            for (int i = 1; i < args.length; i++) {
                st.setString(i, args[i]);
            }
            try (ResultSet rs = st.executeQuery()) {
                ResultSetMetaData md = rs.getMetaData();
                while (rs.next()) {
                    StringBuilder row = new StringBuilder();
                    for (int col = 1; col <= md.getColumnCount(); col++) {
                        if (col > 1) row.append('\t');
                        row.append(rs.getString(col));
                    }
                    System.out.println(row);
                }
            }
        }
    }
}
