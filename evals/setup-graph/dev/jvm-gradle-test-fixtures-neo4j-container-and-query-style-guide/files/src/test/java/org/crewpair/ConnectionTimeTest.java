package org.crewpair;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.crewpair.fixtures.GraphServer;
import org.junit.jupiter.api.Test;

class ConnectionTimeTest {
    @Test
    void noConnectionShorterThanMinimum() throws Exception {
        try (var session = GraphServer.driver().session()) {
            long bad = session.run("MATCH (:Leg)-[c:CONNECTS]->(:Leg) WHERE c.minutes < 35 RETURN count(c) AS n")
                    .single().get("n").asLong();
            assertEquals(0, bad);
        }
    }
}
