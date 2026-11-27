"""Mirror company and holding into Neo4j so later panels can use Cypher."""
from neo4j import GraphDatabase


def sync(conn, uri="bolt://localhost:7687"):
    driver = GraphDatabase.driver(uri)
    with driver.session() as s:
        for owner, owned, pct in conn.execute("SELECT owner_id, owned_id, pct FROM holding"):
            s.run("MERGE (a:Company {id:$a}) MERGE (b:Company {id:$b}) MERGE (a)-[:HOLDS {pct:$p}]->(b)", a=owner, b=owned, p=pct)
