package org.choirbook;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** The one class that holds a driver. Everything else asks it for rows. */
public final class GraphClient implements AutoCloseable {
    private static final QueryConfig READ = QueryConfig.builder().withRouting(RoutingControl.READ).build();
    private final Driver driver;

    public GraphClient() {
        String uri = System.getenv().getOrDefault("CHOIRBOOK_GRAPH_URI", "bolt://localhost:7687");
        this.driver = GraphDatabase.driver(uri, AuthTokens.basic("neo4j", System.getenv("CHOIRBOOK_GRAPH_PASSWORD")));
    }

    public List<Map<String, Object>> read(String query, Map<String, Object> params) {
        return driver.executableQuery(query).withParameters(params).withConfig(READ)
            .execute().records().stream().map(r -> r.asMap()).toList();
    }

    @Override
    public void close() {
        driver.close();
    }
}
