package org.choirbook;

import java.util.List;
import java.util.Map;

/** Which arrangements fit the voices that have signed up. */
public final class Voices {
    private static final String SINGABLE = """
        MATCH (a:Arrangement)-[:NEEDS]->(part:Part)
        WITH a, collect(part.name) AS parts
        WHERE all(p IN parts WHERE p IN $available)
        MATCH (a)-[:ARRANGEMENT_OF]->(piece:Piece)
        RETURN piece.title AS piece, a.arranger AS arranger, parts
        ORDER BY piece
        """;

    private final GraphClient graph;

    public Voices(GraphClient graph) {
        this.graph = graph;
    }

    public List<Map<String, Object>> singableWith(List<String> availableParts) {
        return graph.read(SINGABLE, Map.of("available", availableParts));
    }
}
