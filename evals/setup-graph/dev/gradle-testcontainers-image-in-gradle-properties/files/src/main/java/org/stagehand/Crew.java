package org.stagehand;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

public final class Crew {
    private final Driver driver;

    public Crew(Driver driver) {
        this.driver = driver;
    }

    public List<String> riggersFor(String venue) {
        return driver.executableQuery(
                        "MATCH (p:Person)-[:CERTIFIED_FOR]->(:Venue {name: $v}) RETURN p.name AS name ORDER BY name")
                .withParameters(Map.of("v", venue))
                .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                .execute().records().stream().map(r -> r.get("name").asString()).toList();
    }
}
