"""Customers who bought this also bought: the top pairs of one product."""


def top(conn, product_id, limit=12):
    sql = """SELECT other, orders FROM (
                 SELECT b AS other, orders FROM also_bought WHERE a = :p
                 UNION ALL
                 SELECT a AS other, orders FROM also_bought WHERE b = :p)
             ORDER BY orders DESC, other LIMIT :n"""
    return conn.execute(sql, {"p": product_id, "n": limit}).fetchall()
