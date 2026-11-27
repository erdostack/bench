package org.choirbook.cli;

import org.choirbook.GraphClient;
import org.choirbook.Repertoire;

/** Prints the pieces sung in three or more concerts since the given season. */
public final class SeasonReport {
    public static void main(String[] args) {
        int since = args.length > 0 ? Integer.parseInt(args[0]) : 2024;
        try (var graph = new GraphClient()) {
            new Repertoire(graph).overused(since, 3)
                .forEach(row -> System.out.printf("%-40s %s%n", row.get("piece"), row.get("concerts")));
        }
    }
}
