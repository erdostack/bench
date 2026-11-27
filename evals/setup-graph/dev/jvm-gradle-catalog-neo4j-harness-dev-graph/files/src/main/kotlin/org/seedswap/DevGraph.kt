package org.seedswap

import java.io.File
import org.neo4j.driver.AuthTokens
import org.neo4j.driver.GraphDatabase
import org.neo4j.driver.SessionConfig
import org.neo4j.driver.AccessMode
import org.neo4j.harness.Neo4jBuilders

/** bin/cypher <file> [key=value ...]: in-process Neo4j, fixture loaded, one read query, then shut down. */
fun main(args: Array<String>) {
    require(args.isNotEmpty()) { "usage: bin/cypher <file.cypher> [key=value ...]" }
    val params = args.drop(1).associate { it.substringBefore('=') to it.substringAfter('=') }
    Neo4jBuilders.newInProcessBuilder()
        .withFixture(File("seed/fixture.cypher").readText())
        .build().use { neo4j ->
            GraphDatabase.driver(neo4j.boltURI(), AuthTokens.none()).use { driver ->
                driver.session(SessionConfig.builder().withDefaultAccessMode(AccessMode.READ).build()).use { s ->
                    s.run(File(args[0]).readText(), params).list().forEach { println(it.asMap()) }
                }
            }
        }
}
