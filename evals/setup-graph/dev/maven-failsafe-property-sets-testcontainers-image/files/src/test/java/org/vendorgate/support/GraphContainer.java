package org.vendorgate.support;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.testcontainers.containers.Neo4jContainer;
import org.testcontainers.utility.DockerImageName;

/** One seeded container per JVM, shared by every integration test. */
public final class GraphContainer {
    private static Neo4jContainer<?> container;

    private GraphContainer() {}

    public static synchronized Driver driver() throws Exception {
        if (container == null) {
            String image = System.getProperty("graph.image", "neo4j:5.26.24-community");
            container = new Neo4jContainer<>(DockerImageName.parse(image).asCompatibleSubstituteFor("neo4j"))
                    .withAdminPassword("integration-only");
            container.start();
            try (var d = GraphDatabase.driver(container.getBoltUrl(), AuthTokens.basic("neo4j", "integration-only"))) {
                for (String stmt : Files.readString(Path.of("src/test/resources/seed.cypher")).split(";")) {
                    if (!stmt.isBlank()) {
                        d.executableQuery(stmt).execute();
                    }
                }
            }
        }
        return GraphDatabase.driver(container.getBoltUrl(), AuthTokens.basic("neo4j", "integration-only"));
    }
}
