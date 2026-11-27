package org.coldchain.it;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.testcontainers.containers.Neo4jContainer;
import org.testcontainers.utility.DockerImageName;

/** One throwaway graph per JVM, shared by every integration test and by bin/q. */
public final class GraphFixture {
    static final Neo4jContainer<?> NEO4J =
            new Neo4jContainer<>(DockerImageName.parse("neo4j:5.26.24-community")).withoutAuthentication();

    private static Driver driver;

    static synchronized Driver driver() throws Exception {
        if (driver == null) {
            NEO4J.start();
            driver = GraphDatabase.driver(NEO4J.getBoltUrl(), AuthTokens.none());
            try (var session = driver.session()) {
                for (String stmt : Files.readString(Path.of("src/test/resources/fixture.cypher")).split(";")) {
                    if (!stmt.isBlank()) session.run(stmt).consume();
                }
            }
        }
        return driver;
    }

    private GraphFixture() {
    }
}
