package org.choirbook;

import java.util.List;
import java.util.Map;

/** Checks a draft programme against what was sung recently. */
public final class Programme {
    private static final String REPEATS = """
        UNWIND $titles AS title
        MATCH (p:Piece {title: title})<-[:ARRANGEMENT_OF*0..1]-()<-[:INCLUDES]-(c:Concert {season: $lastSeason})
        RETURN title, collect(DISTINCT c.name) AS concerts
        """;

    private final GraphClient graph;

    public Programme(GraphClient graph) {
        this.graph = graph;
    }

    public List<Map<String, Object>> repeatsFrom(int lastSeason, List<String> titles) {
        return graph.read(REPEATS, Map.of("titles", titles, "lastSeason", lastSeason));
    }
}
