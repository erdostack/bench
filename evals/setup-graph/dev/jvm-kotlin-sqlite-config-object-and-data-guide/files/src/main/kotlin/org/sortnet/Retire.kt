package org.sortnet

/** bin/retire <code>: removes a closed centre (docs/DATA.md: fails while it still has legs). */
fun main(args: Array<String>) {
    Db.open().use { conn ->
        conn.prepareStatement("DELETE FROM centre WHERE code = ?").use { st ->
            st.setString(1, args.single())
            println("removed ${st.executeUpdate()} centre(s)")
        }
    }
}
