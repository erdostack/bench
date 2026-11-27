package org.crewpair.fixtures;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.testcontainers.containers.Neo4jContainer;
import org.testcontainers.utility.DockerImageName;

/** The one graph every test and bin/q use: started once per JVM, loaded with seed/legs.cypher. */
public final class GraphServer {
    private static final Neo4jContainer<?> CONTAINER =
            new Neo4jContainer<>(DockerImageName.parse("neo4j:2026.04.0-community"))
                    .withoutAuthentication()
                    // same default as the hosted database, which predates the 2026 upgrades
                    .withNeo4jConfig("db.query.default_language", "CYPHER_5");

    private static Driver driver;

    public static synchronized Driver driver() throws Exception {
        if (driver == null) {
            CONTAINER.start();
            driver = GraphDatabase.driver(CONTAINER.getBoltUrl(), AuthTokens.none());
            try (var session = driver.session()) {
                for (String stmt : Files.readString(Path.of("seed/legs.cypher")).split(";")) {
                    if (!stmt.isBlank()) session.run(stmt).consume();
                }
            }
        }
        return driver;
    }

    private GraphServer() {
    }
}
