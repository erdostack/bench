package org.seedvault.lineage;

import org.neo4j.driver.GraphDatabase;

/** Recreates the constraint the lineage queries rely on; the accession export is loaded by the ops job. */
public final class Load {
    public static void main(String[] args) {
        try (var driver = GraphDatabase.driver("bolt://localhost:7687")) {
            driver.executableQuery(
                    "CREATE CONSTRAINT accession_code IF NOT EXISTS FOR (a:Accession) REQUIRE a.code IS UNIQUE")
                .execute();
        }
    }
}
