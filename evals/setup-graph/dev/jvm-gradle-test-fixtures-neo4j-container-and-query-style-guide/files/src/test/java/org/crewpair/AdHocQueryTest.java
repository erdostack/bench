package org.crewpair;

import java.nio.file.Files;
import java.nio.file.Path;
import org.crewpair.fixtures.GraphServer;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Tag("adhoc")
class AdHocQueryTest {
    @Test
    void run() throws Exception {
        String file = System.getProperty("cypher.file");
        try (var session = GraphServer.driver().session()) {
            session.executeRead(tx -> tx.run(Files.readString(Path.of(file))).list())
                    .forEach(r -> System.out.println(r.asMap()));
        }
    }
}
