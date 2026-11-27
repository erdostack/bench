package org.gridline;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/** The one place connections to data/grid.db are opened. */
public final class Db {
    private Db() {}

    public static Connection open(Path file) throws SQLException {
        Connection con = DriverManager.getConnection("jdbc:sqlite:" + file);
        con.setAutoCommit(true);
        return con;
    }
}
