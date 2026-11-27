package org.seedbank;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class QueriesTest {
    @Test
    void everySavedQueryReturnsSomething() throws Exception {
        try (var files = Files.list(Path.of("src/main/resources/queries"))) {
            for (Path file : files.toList()) {
                assertTrue(Files.readString(file).contains("RETURN"), file.toString());
            }
        }
    }
}
