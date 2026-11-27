from neo4j import GraphDatabase


def sync(conn, uri="bolt://localhost:7687"):
    driver = GraphDatabase.driver(uri)
    with driver.session() as s:
        for kit_id, item_id, qty in conn.execute("SELECT kit_id, item_id, qty FROM kit_line"):
            s.run("MERGE (k:Item {id: $k}) MERGE (i:Item {id: $i}) MERGE (k)-[:HOLDS {qty: $q}]->(i)", k=kit_id, i=item_id, q=qty)
