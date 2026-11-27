package shop.recs;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;

final class AlsoBought {
    private static final String QUERY = """
        MATCH (p:Product {sku: $sku})<-[:CONTAINS]-(:Order)-[:CONTAINS]->(other:Product)
        WHERE other <> p
        RETURN other.sku AS sku, count(*) AS together
        ORDER BY together DESC
        LIMIT $limit
        """;

    private final Driver driver;

    AlsoBought(Driver driver) {
        this.driver = driver;
    }

    List<String> forSku(String sku, int limit) {
        return driver.executableQuery(QUERY)
            .withParameters(Map.of("sku", sku, "limit", limit))
            .execute()
            .records().stream().map(r -> r.get("sku").asString()).toList();
    }
}
