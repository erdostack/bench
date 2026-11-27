package org.gridline;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.ResultSet;

/** Runs one .sql file against data/grid.db and prints the rows tab-separated. */
public final class RunSql {
    private RunSql() {}

    public static void main(String[] args) throws Exception {
        String sql = Files.readString(Path.of(args[0]));
        try (var con = Db.open(Path.of("data/grid.db")); var st = con.prepareStatement(sql)) {
            if (args.length > 1) {
                st.setString(1, args[1]);
            }
            try (ResultSet rs = st.executeQuery()) {
                int n = rs.getMetaData().getColumnCount();
                while (rs.next()) {
                    StringBuilder row = new StringBuilder();
                    for (int i = 1; i <= n; i++) {
                        row.append(i > 1 ? "\t" : "").append(rs.getString(i));
                    }
                    System.out.println(row);
                }
            }
        }
    }
}
