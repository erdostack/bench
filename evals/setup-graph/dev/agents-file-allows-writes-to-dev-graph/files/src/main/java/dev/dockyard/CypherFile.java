package dev.dockyard;

import java.nio.file.Files;
import java.nio.file.Path;

/** Runs every statement of one .cypher file and prints the rows. */
public final class CypherFile {
    public static void main(String[] args) throws Exception {
        if (args.length != 1 || args[0].isBlank()) {
            System.err.println("usage: ./gradlew cypher -Pfile=<path to .cypher>");
            System.exit(2);
        }
        try (var driver = Graph.open()) {
            for (String statement : Files.readString(Path.of(args[0])).split(";\\s*\\n")) {
                if (!statement.isBlank()) {
                    driver.executableQuery(statement).execute().records().forEach(r -> System.out.println(r.asMap()));
                }
            }
        }
    }
}
