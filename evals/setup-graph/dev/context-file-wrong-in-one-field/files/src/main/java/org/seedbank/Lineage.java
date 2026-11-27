package org.seedbank;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;
import org.neo4j.driver.RoutingControl;

/** Where did this lot come from? */
public final class Lineage {
    private static final String ANCESTORS = """
        MATCH (lot:Lot {code: $code})-[:GROWN_FROM*1..12]->(ancestor:Lot)
        OPTIONAL MATCH (ancestor)-[:DONATED_BY]->(d:Donor)
        RETURN ancestor.code AS code, ancestor.year AS year, d.name AS donor
        ORDER BY year DESC
        """;

    private final Driver driver;

    public Lineage(Driver driver) {
        this.driver = driver;
    }

    public List<Map<String, Object>> ancestors(String lotCode) {
        return driver.executableQuery(ANCESTORS)
            .withParameters(Map.of("code", lotCode))
            .withConfig(org.neo4j.driver.QueryConfig.builder().withRouting(RoutingControl.READ).build())
            .execute().records().stream().map(r -> r.asMap()).toList();
    }
}
