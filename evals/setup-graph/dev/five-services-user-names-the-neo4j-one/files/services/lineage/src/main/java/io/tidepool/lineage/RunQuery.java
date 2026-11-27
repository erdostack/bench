package io.tidepool.lineage;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

/** Entry point of the runQuery Gradle task and bin/lq. */
public final class RunQuery {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("usage: bin/lq <file.cypher> [name=value ...]");
            System.exit(2);
        }
        Map<String, Object> parameters = new HashMap<>();
        if (args.length > 1 && !args[1].isBlank()) {
            for (String pair : args[1].split(",")) {
                String[] parts = pair.split("=", 2);
                parameters.put(parts[0], parts[1]);
            }
        }
        try (LineageGraph graph = new LineageGraph()) {
            graph.read(Files.readString(Path.of(args[0])), parameters).forEach(System.out::println);
        }
    }
}
