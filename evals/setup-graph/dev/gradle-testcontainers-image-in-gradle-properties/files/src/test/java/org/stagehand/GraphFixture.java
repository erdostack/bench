package org.stagehand;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.testcontainers.containers.Neo4jContainer;
import org.testcontainers.utility.DockerImageName;

final class GraphFixture {
    private static Neo4jContainer<?> container;

    private GraphFixture() {}

    static synchronized Driver driver() throws Exception {
        if (container == null) {
            String image = System.getProperty("graph.image", "neo4j:5.26.25");
            container = new Neo4jContainer<>(DockerImageName.parse(image).asCompatibleSubstituteFor("neo4j"))
                    .withoutAuthentication()
                    .withEnv("NEO4J_ACCEPT_LICENSE_AGREEMENT", System.getProperty("neo4j.accept.license", "no"));
            container.start();
            try (var d = GraphDatabase.driver(container.getBoltUrl(), AuthTokens.none())) {
                for (String stmt : Files.readString(Path.of("src/test/resources/seed.cypher")).split(";")) {
                    if (!stmt.isBlank()) {
                        d.executableQuery(stmt).execute();
                    }
                }
            }
        }
        return GraphDatabase.driver(container.getBoltUrl(), AuthTokens.none());
    }
}
