package org.sortnet

import java.sql.Connection
import java.sql.DriverManager
import org.sqlite.SQLiteConfig

object Db {
    private val config = SQLiteConfig().apply {
        enforceForeignKeys(true)
        setBusyTimeout(5_000)
    }

    fun open(path: String = "data/routes.db"): Connection =
        DriverManager.getConnection("jdbc:sqlite:$path")
}
