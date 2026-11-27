package org.coldchain.it;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;
import org.neo4j.driver.SessionConfig;

/** Not a test: bin/q runs one query file against the fixture graph through this class. */
class AdHocQueryIT {
    @Test
    void run() throws Exception {
        String file = System.getProperty("cypher.file");
        Assumptions.assumeTrue(file != null, "set -Dcypher.file (bin/q does)");
        try (var session = GraphFixture.driver().session(SessionConfig.defaultConfig())) {
            session.executeRead(tx -> tx.run(Files.readString(Path.of(file))).list())
                    .forEach(r -> System.out.println(r.asMap()));
        }
    }
}
