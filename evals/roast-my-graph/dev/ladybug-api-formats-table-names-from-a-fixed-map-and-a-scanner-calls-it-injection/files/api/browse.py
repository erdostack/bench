"""Generic handlers. Every value that comes from a request is passed as a query parameter."""
from .catalog import LINKS, TABLES

MAX_PAGE = 200


class NotFound(Exception):
    pass


def _table(kind):
    try:
        return TABLES[kind]
    except KeyError:
        raise NotFound(kind) from None


def list_nodes(conn, kind, skip=0, limit=50):
    table, key, columns = _table(kind)
    skip = max(0, int(skip))
    limit = min(max(1, int(limit)), MAX_PAGE)
    shown = ", ".join(f"n.{c} AS {c}" for c in columns)
    query = f"MATCH (n:{table}) RETURN {shown} ORDER BY n.{key} SKIP $skip LIMIT $limit"
    return conn.execute(query, {"skip": skip, "limit": limit}).get_all()


def get_node(conn, kind, key_value):
    table, key, columns = _table(kind)
    shown = ", ".join(f"n.{c} AS {c}" for c in columns)
    query = f"MATCH (n:{table}) WHERE n.{key} = $value RETURN {shown}"
    rows = conn.execute(query, {"value": str(key_value)}).get_all()
    if not rows:
        raise NotFound(key_value)
    return rows[0]


def follow(conn, link, key_value, limit=50):
    try:
        src, rel, dst = LINKS[link]
    except KeyError:
        raise NotFound(link) from None
    _, src_key, _ = next(v for v in TABLES.values() if v[0] == src)
    _, dst_key, dst_columns = next(v for v in TABLES.values() if v[0] == dst)
    limit = min(max(1, int(limit)), MAX_PAGE)
    shown = ", ".join(f"b.{c} AS {c}" for c in dst_columns)
    query = (f"MATCH (a:{src})-[:{rel}]->(b:{dst}) WHERE a.{src_key} = $value "
             f"RETURN {shown} ORDER BY b.{dst_key} LIMIT $limit")
    return conn.execute(query, {"value": str(key_value), "limit": limit}).get_all()
