package org.choirbook;

import java.util.List;
import java.util.Map;

/** What has the choir sung, and how often. */
public final class Repertoire {
    private static final String OVERUSED = """
        MATCH (p:Piece)<-[:ARRANGEMENT_OF*0..1]-(sung)<-[:INCLUDES]-(c:Concert)
        WHERE c.season >= $since
        WITH p, count(DISTINCT c) AS concerts
        WHERE concerts >= $threshold
        RETURN p.title AS piece, concerts
        ORDER BY concerts DESC, piece
        """;

    private final GraphClient graph;

    public Repertoire(GraphClient graph) {
        this.graph = graph;
    }

    public List<Map<String, Object>> overused(int sinceSeason, int threshold) {
        return graph.read(OVERUSED, Map.of("since", sinceSeason, "threshold", threshold));
    }
}
