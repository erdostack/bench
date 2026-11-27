package org.relaymesh;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;

/** ./gradlew cypher -Pfile=<file>: one query against the compose graph, rows to stdout. */
public final class RunCypher {
    public static void main(String[] args) throws Exception {
        String query = Files.readString(Path.of(args[0]));
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.none());
             var session = driver.session()) {
            session.run(query).list().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
