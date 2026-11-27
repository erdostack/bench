package shop.recs;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.GraphDatabase;

public final class Main {
    public static void main(String[] args) {
        String password = System.getenv("RECS_GRAPH_PASSWORD");
        try (var driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", password))) {
            new AlsoBought(driver).forSku(args.length > 0 ? args[0] : "SKU-1042", 5).forEach(System.out::println);
        }
    }
}
