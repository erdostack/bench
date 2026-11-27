package org.relaymesh;

import java.nio.file.Files;
import java.nio.file.Path;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;

/** Reloads seed/mesh.cypher into an empty graph. */
public final class LoadMesh {
    public static void main(String[] args) throws Exception {
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.none());
             var session = driver.session()) {
            session.run("MATCH (n) DETACH DELETE n").consume();
            for (String stmt : Files.readString(Path.of("seed/mesh.cypher")).split(";")) {
                if (!stmt.isBlank()) session.run(stmt).consume();
            }
        }
    }
}
