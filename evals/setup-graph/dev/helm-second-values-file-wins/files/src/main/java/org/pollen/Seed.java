package org.pollen;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;

/** Wipes the local graph and loads a small generated season of hive moves. */
public final class Seed {
    private Seed() {}

    public static void main(String[] args) {
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.none())) {
            driver.executableQuery("MATCH (n) DETACH DELETE n").execute();
            driver.executableQuery("UNWIND range(1, 30) AS i "
                    + "CREATE (:Hive {id: i})-[:PLACED_IN {week: i % 12}]->(:Orchard {id: i % 7})").execute();
        }
    }
}
