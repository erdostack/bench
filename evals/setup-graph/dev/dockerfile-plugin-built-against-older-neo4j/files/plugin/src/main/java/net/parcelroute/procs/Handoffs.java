package net.parcelroute.procs;

import java.util.stream.Stream;
import org.neo4j.graphdb.Transaction;
import org.neo4j.procedure.Context;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.Procedure;

public class Handoffs {
    @Context
    public Transaction tx;

    public record Leg(String from, String to, long cost) {}

    @Procedure("parcel.handoffs")
    public Stream<Leg> handoffs(@Name("from") String from, @Name("to") String to,
                                @Name(value = "maxLegs", defaultValue = "6") long maxLegs) {
        // Dijkstra over TRUNK relationships with a fixed hand-off cost; omitted here for brevity.
        return Stream.empty();
    }
}
