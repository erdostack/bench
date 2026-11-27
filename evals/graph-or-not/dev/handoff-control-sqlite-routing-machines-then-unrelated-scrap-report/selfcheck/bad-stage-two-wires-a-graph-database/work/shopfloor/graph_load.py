from neo4j import GraphDatabase


def load(conn):
    with GraphDatabase.driver("bolt://localhost:7687").session() as s:
        for p, m in conn.execute("SELECT DISTINCT product_id, machine_id FROM routing_op"):
            s.run("MERGE (p:Product {id: $p}) MERGE (m:Machine {id: $m}) MERGE (p)-[:USES]->(m)", p=p, m=m)
