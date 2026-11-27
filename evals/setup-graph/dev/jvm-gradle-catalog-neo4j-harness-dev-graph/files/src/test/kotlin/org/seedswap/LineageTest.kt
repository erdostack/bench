package org.seedswap

import java.io.File
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test
import org.neo4j.harness.Neo4jBuilders

class LineageTest {
    @Test
    fun fixtureHasEveryLibrary() {
        Neo4jBuilders.newInProcessBuilder().withFixture(File("seed/fixture.cypher").readText()).build().use { neo4j ->
            val n = neo4j.defaultDatabaseService().executeTransactionally(
                "MATCH (l:Library) RETURN count(l) AS n", emptyMap()) { it.next()["n"] as Long }
            assertEquals(5L, n)
        }
    }
}
