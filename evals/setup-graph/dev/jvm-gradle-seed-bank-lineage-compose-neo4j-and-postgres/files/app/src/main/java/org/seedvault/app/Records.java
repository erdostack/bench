package org.seedvault.app;

import java.sql.DriverManager;

/** Germination tests per accession, from the records database. */
public final class Records {
    public static void main(String[] args) throws Exception {
        try (var c = DriverManager.getConnection("jdbc:postgresql://localhost:5432/records", "seedvault", "dev");
             var rs = c.createStatement().executeQuery("SELECT code, tested_on, germinated_pct FROM germination")) {
            while (rs.next()) System.out.println(rs.getString(1) + " " + rs.getDate(2) + " " + rs.getInt(3));
        }
    }
}
