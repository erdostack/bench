def split_cost(conn, a, b):
    faction = dict(conn.execute("SELECT id, faction FROM member"))
    return sum(c for x, y, c in conn.execute("SELECT a, b, contexts FROM tie") if faction[x] != faction[y])
