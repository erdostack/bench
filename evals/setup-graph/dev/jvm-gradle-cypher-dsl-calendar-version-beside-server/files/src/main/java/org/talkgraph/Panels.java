package org.talkgraph;

import org.neo4j.cypherdsl.core.Cypher;

/** Builds the panel query with Cypher-DSL. */
final class Panels {
    private Panels() {}

    static String query() {
        var s = Cypher.node("Speaker").named("s");
        var t = Cypher.node("Topic").named("t");
        return Cypher.match(s.relationshipTo(t, "SPEAKS_ON")).returning(s, t).build().getCypher();
    }
}
