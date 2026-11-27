package org.ridgeway;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/** The one place a connection to the trail database is opened. */
public final class Trails {
    private Trails() {}

    public static Connection open() throws SQLException {
        return DriverManager.getConnection("jdbc:sqlite:data/trails.db");
    }
}
