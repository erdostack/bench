package org.mutualaid

import java.io.File
import org.neo4j.driver.Driver
import org.neo4j.driver.SessionConfig
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component

/** bin/cypher <file>: runs one read query once the app (and its compose-managed graph) is up. */
@Component
class CypherRunner(
    private val driver: Driver,
    @Value("\${cypher.file:}") private val file: String,
) : CommandLineRunner {
    override fun run(vararg args: String) {
        if (file.isBlank()) return
        driver.session(SessionConfig.defaultConfig()).use { s ->
            s.executeRead { tx -> tx.run(File(file).readText()).list() }.forEach { println(it.asMap()) }
        }
    }
}
