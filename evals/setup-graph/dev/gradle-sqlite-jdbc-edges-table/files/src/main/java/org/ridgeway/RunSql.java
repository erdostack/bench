package org.ridgeway;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.ResultSet;

/** Runs one SQL file and prints each row tab-separated. */
public final class RunSql {
    private RunSql() {}

    public static void main(String[] args) throws Exception {
        String sql = Files.readString(Path.of(args[0]));
        try (var con = Trails.open(); var st = con.createStatement(); ResultSet rs = st.executeQuery(sql)) {
            int n = rs.getMetaData().getColumnCount();
            while (rs.next()) {
                var row = new StringBuilder();
                for (int i = 1; i <= n; i++) {
                    row.append(i > 1 ? "\t" : "").append(rs.getString(i));
                }
                System.out.println(row);
            }
        }
    }
}
