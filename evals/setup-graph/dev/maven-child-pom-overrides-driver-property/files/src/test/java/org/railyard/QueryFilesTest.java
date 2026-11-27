package org.railyard;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class QueryFilesTest {
    @Test
    void everyQueryUsesKnownRelationshipTypes() throws Exception {
        try (var files = Files.list(Path.of("queries"))) {
            for (Path p : files.toList()) {
                String body = Files.readString(p);
                assertTrue(Fleet.RELS.stream().anyMatch(body::contains), p.toString());
            }
        }
    }
}
