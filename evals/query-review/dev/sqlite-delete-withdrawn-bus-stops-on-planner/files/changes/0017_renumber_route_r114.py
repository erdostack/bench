"""0017: route R-114 now calls at ST-2210 before ST-2209 (new one-way system). Reviewed: k.osei. Applied to planner 2026-09-02."""


def run(conn):
    n = 0
    with conn:
        route = conn.execute("SELECT id FROM nodes WHERE kind = 'route' AND code = 'R-114'").fetchone()[0]
        for code, seq in (("ST-2210", 7), ("ST-2209", 8)):
            n += conn.execute("UPDATE edges SET seq = ? WHERE kind = 'serves' AND src = ? AND seq <> ? AND dst = "
                              "(SELECT id FROM nodes WHERE kind = 'stop' AND code = ?)", (seq, route, seq, code)).rowcount
    return n
