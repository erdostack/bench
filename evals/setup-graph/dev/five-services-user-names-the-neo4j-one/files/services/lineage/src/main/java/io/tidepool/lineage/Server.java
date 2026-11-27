package io.tidepool.lineage;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import io.javalin.Javalin;

public final class Server {
    public static void main(String[] args) {
        LineageGraph graph = new LineageGraph();
        Javalin app = Javalin.create();
        app.get("/figures/{figure}/upstream", ctx -> ctx.json(
                graph.read(Files.readString(Path.of("queries/upstream_of.cypher")), Map.of("figure", ctx.pathParam("figure")))));
        app.get("/datasets/{dataset}/impact", ctx -> ctx.json(
                graph.read(Files.readString(Path.of("queries/impact_of.cypher")), Map.of("dataset", ctx.pathParam("dataset")))));
        app.start(8103);
    }
}
