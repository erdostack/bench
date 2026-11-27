package org.choirbook;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class QueryTextTest {
    @Test
    void savedQueriesAreBounded() throws Exception {
        try (var files = Files.list(Path.of("..", "queries"))) {
            for (Path file : files.toList()) {
                String text = Files.readString(file);
                assertTrue(!text.contains("*]") && !text.contains("*)"), "unbounded pattern in " + file);
            }
        }
    }
}
