package org.shelfmark;

import java.util.Collection;
import java.util.Map;
import org.springframework.data.neo4j.core.Neo4jClient;
import org.springframework.stereotype.Service;

@Service
public class LoanRoutes {
    private final Neo4jClient client;

    public LoanRoutes(Neo4jClient client) {
        this.client = client;
    }

    public Collection<Map<String, Object>> chain(String from, String to) {
        return client.query("MATCH p = shortestPath((a:Branch {code: $from})-[:COURIER*..8]-(b:Branch {code: $to})) "
                + "RETURN [n IN nodes(p) | n.code] AS branches").bindAll(Map.of("from", from, "to", to)).fetch().all();
    }
}
