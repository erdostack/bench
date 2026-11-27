package org.seedbank;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;

/** Which gardens have tried a variety, and how did it go. */
public final class Trials {
    private static final String BY_VARIETY = """
        MATCH (v:Variety {name: $variety})<-[:OF_VARIETY]-(:Lot)<-[:SOWED]-(t:Trial)-[:AT]->(g:Garden)
        RETURN g.name AS garden, t.year AS year, t.outcome AS outcome
        ORDER BY year DESC, garden
        """;

    private final Driver driver;

    public Trials(Driver driver) {
        this.driver = driver;
    }

    public List<Map<String, Object>> byVariety(String variety) {
        return driver.executableQuery(BY_VARIETY).withParameters(Map.of("variety", variety))
            .execute().records().stream().map(r -> r.asMap()).toList();
    }
}
