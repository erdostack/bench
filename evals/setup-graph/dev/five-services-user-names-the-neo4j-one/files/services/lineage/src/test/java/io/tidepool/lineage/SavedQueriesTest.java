package io.tidepool.lineage;

import static org.junit.jupiter.api.Assertions.assertFalse;

import java.nio.file.Files;
import java.nio.file.Path;

import org.junit.jupiter.api.Test;

class SavedQueriesTest {
    @Test
    void savedQueriesDoNotWrite() throws Exception {
        try (var paths = Files.list(Path.of("queries"))) {
            for (Path path : paths.toList()) {
                String text = Files.readString(path).toUpperCase();
                assertFalse(text.contains("MERGE ") || text.contains("CREATE ") || text.contains("DELETE "), path.toString());
            }
        }
    }
}
