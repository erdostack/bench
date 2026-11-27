"""Permanently delete cards trashed before CUTOFF and everything attached to them."""
CUTOFF = "2026-10-24"
CHUNK = 1000


def _delete(conn, table, key, ids):
    for i in range(0, len(ids), CHUNK):
        with conn:
            conn.executemany(f"DELETE FROM {table} WHERE {key} = ?", [(x,) for x in ids[i:i + CHUNK]])


def run(conn):
    cards = [r[0] for r in conn.execute("SELECT id FROM cards WHERE trashed_at < ? ORDER BY id", (CUTOFF,))]
    gone = set(cards)
    # Attached by card id, not by trashed_at: an arrow restored on its own has trashed_at NULL even
    # though its card is in the trash, and frame memberships are never trashed.
    conns = [r[0] for r in conn.execute("SELECT id, from_card, to_card FROM connectors")
             if r[1] in gone or r[2] in gone]
    members = [r[0] for r in conn.execute("SELECT rowid, frame_id, card_id FROM frame_members")
               if r[1] in gone or r[2] in gone]
    _delete(conn, "connectors", "id", conns)
    _delete(conn, "frame_members", "rowid", members)
    _delete(conn, "cards", "id", cards)
    return len(cards)
