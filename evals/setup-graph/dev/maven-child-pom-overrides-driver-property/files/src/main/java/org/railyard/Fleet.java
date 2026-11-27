package org.railyard;

import java.util.List;

/** Labels and relationship types the queries rely on; kept here so tests can check the .cypher files. */
public final class Fleet {
    private Fleet() {}

    public static final List<String> LABELS = List.of("Wagon", "Bogie", "Component", "Depot");
    public static final List<String> RELS = List.of("RIDES_ON", "FITTED_WITH", "SERVICES");
}
