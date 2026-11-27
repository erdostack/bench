package org.coldchain;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;
import org.neo4j.driver.SessionConfig;

/** Reads hand-off chains for one shipment. */
public final class HandoffRepository {
    private final Driver driver;

    public HandoffRepository(Driver driver) {
        this.driver = driver;
    }

    public List<Map<String, Object>> chain(String shipmentId) {
        try (var session = driver.session(SessionConfig.defaultConfig())) {
            return session.executeRead(tx -> tx.run(
                    "MATCH p = (:Depot)-[:HANDED_TO*]->(c:Clinic) WHERE all(r IN relationships(p) WHERE r.shipment = $id) "
                            + "RETURN [n IN nodes(p) | n.name] AS chain",
                    Map.of("id", shipmentId)).list(r -> r.asMap()));
        }
    }
}
