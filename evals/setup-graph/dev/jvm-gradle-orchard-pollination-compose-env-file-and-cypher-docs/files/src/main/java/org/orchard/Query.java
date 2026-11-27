package org.orchard;

import java.nio.file.Files;
import java.nio.file.Path;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.SessionConfig;
import org.neo4j.driver.AccessMode;

/** Runs one read query from a file and prints each record. */
public final class Query {
    public static void main(String[] args) throws Exception {
        String cypher = Files.readString(Path.of(args[0]));
        String password = System.getenv().getOrDefault("ORCHARD_PASSWORD", "");
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", password));
             var session = driver.session(SessionConfig.builder().withDefaultAccessMode(AccessMode.READ).build())) {
            session.run(cypher).forEachRemaining(r -> System.out.println(r.values()));
        }
    }
}
