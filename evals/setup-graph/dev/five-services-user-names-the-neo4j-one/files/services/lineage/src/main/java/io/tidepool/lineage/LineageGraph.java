package io.tidepool.lineage;

import java.util.List;
import java.util.Map;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.QueryConfig;
import org.neo4j.driver.RoutingControl;

/** The lineage service's own graph database (dev/compose.yaml locally). Reads only. */
public final class LineageGraph implements AutoCloseable {
    private final Driver driver;

    public LineageGraph() {
        String uri = System.getenv().getOrDefault("LINEAGE_GRAPH_URI", "bolt://localhost:7689");
        String password = System.getenv("LINEAGE_GRAPH_PASSWORD");
        if (password == null) {
            throw new IllegalStateException("LINEAGE_GRAPH_PASSWORD is not set");
        }
        this.driver = GraphDatabase.driver(uri, AuthTokens.basic("neo4j", password));
    }

    public List<Map<String, Object>> read(String cypher, Map<String, Object> parameters) {
        return driver.executableQuery(cypher)
                .withParameters(parameters)
                .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
                .execute()
                .records().stream().map(record -> record.asMap()).toList();
    }

    @Override
    public void close() {
        driver.close();
    }
}
