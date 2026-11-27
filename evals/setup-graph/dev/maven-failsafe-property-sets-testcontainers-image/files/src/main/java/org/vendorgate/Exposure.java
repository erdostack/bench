package org.vendorgate;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** Read-only questions about the supplier graph. */
public final class Exposure {
    private final Driver driver;

    public Exposure(Driver driver) {
        this.driver = driver;
    }

    public List<String> productLinesAtRisk(String factory) {
        return driver.executableQuery(
                        "MATCH (f:Factory {code: $f})<-[:SOURCES_FROM*1..4]-(:Supplier)<-[:BUYS_FROM]-(l:ProductLine) "
                                + "RETURN DISTINCT l.name AS line ORDER BY line")
                .withParameters(Map.of("f", factory))
                .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                .execute().records().stream().map(r -> r.get("line").asString()).toList();
    }
}
