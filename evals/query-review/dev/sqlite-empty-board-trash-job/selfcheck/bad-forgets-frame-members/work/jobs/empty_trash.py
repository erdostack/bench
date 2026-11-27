"""Permanently delete cards trashed before CUTOFF and their connectors."""
CUTOFF = "2026-10-24"
CHUNK = 1000


def run(conn):
    cards = [r[0] for r in conn.execute("SELECT id FROM cards WHERE trashed_at < ? ORDER BY id", (CUTOFF,))]
    gone = set(cards)
    conns = [r[0] for r in conn.execute("SELECT id, from_card, to_card FROM connectors") if r[1] in gone or r[2] in gone]
    for ids, table in ((conns, "connectors"), (cards, "cards")):
        for i in range(0, len(ids), CHUNK):
            with conn:
                conn.executemany(f"DELETE FROM {table} WHERE id = ?", [(x,) for x in ids[i:i + CHUNK]])
    return len(cards)
