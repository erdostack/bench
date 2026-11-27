package org.crewpair;

import java.util.List;
import java.util.Map;
import org.neo4j.driver.Driver;

public final class PairingReader {
    private final Driver driver;

    public PairingReader(Driver driver) {
        this.driver = driver;
    }

    public List<Map<String, Object>> fromBase(String base) {
        try (var session = driver.session()) {
            return session.executeRead(tx -> tx.run(
                    "MATCH p = (a:Leg {origin: $base})-[:CONNECTS*1..4]->(b:Leg {destination: $base}) "
                            + "RETURN [l IN nodes(p) | l.flight] AS legs", Map.of("base", base)).list(r -> r.asMap()));
        }
    }
}
