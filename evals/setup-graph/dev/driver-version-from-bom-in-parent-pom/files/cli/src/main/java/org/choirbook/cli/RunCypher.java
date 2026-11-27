package org.choirbook.cli;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import org.choirbook.GraphClient;

/** Runs one .cypher file read-only and prints each row. Used by bin/cypher. */
public final class RunCypher {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: bin/cypher <file.cypher>");
            System.exit(2);
        }
        try (var graph = new GraphClient()) {
            graph.read(Files.readString(Path.of(args[0])), Map.of()).forEach(System.out::println);
        }
    }
}
