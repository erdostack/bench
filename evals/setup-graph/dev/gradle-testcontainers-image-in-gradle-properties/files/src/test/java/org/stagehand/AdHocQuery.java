package org.stagehand;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** Used by ./gradlew adhoc to run one query file; skipped by ./gradlew test. */
class AdHocQuery {
    @Test
    void run() throws Exception {
        String file = System.getProperty("query.file", "");
        if (file.isBlank()) {
            return;
        }
        try (var driver = GraphFixture.driver()) {
            driver.executableQuery(Files.readString(Path.of(file)))
                    .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                    .execute().records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
