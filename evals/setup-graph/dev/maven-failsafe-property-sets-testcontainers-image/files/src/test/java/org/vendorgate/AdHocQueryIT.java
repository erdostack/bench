package org.vendorgate;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;
import org.vendorgate.support.GraphContainer;

/** Not a test: bin/q uses it to run one query file against the seeded container. */
class AdHocQueryIT {
    @Test
    void run() throws Exception {
        String file = System.getProperty("query.file");
        if (file == null) {
            return;
        }
        try (var driver = GraphContainer.driver()) {
            driver.executableQuery(Files.readString(Path.of(file)))
                    .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                    .execute().records().forEach(r -> System.out.println(r.asMap()));
        }
    }
}
