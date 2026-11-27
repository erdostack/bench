package org.sortnet

import java.io.File

/** bin/sql <file.sql> [arg ...]: one query, tab-separated rows. */
fun main(args: Array<String>) {
    require(args.isNotEmpty()) { "usage: bin/sql <file.sql> [arg ...]" }
    Db.open().use { conn ->
        val st = conn.prepareStatement(File(args[0]).readText())
        args.drop(1).forEachIndexed { i, a -> st.setString(i + 1, a) }
        val rs = st.executeQuery()
        val n = rs.metaData.columnCount
        while (rs.next()) println((1..n).joinToString("\t") { rs.getString(it) ?: "" })
    }
}
