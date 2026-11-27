package org.mutualaid

import java.io.File
import org.neo4j.driver.Driver
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component

/** bin/seed: loads seed/stations.cypher into an empty local graph. */
@Component
class SeedRunner(private val driver: Driver, @Value("\${seed:false}") private val seed: Boolean) : CommandLineRunner {
    override fun run(vararg args: String) {
        if (!seed) return
        driver.session().use { s ->
            File("seed/stations.cypher").readText().split(';').filter { it.isNotBlank() }.forEach { s.run(it).consume() }
        }
    }
}
