"""Permanently delete cards (and their trashed connectors) trashed before CUTOFF."""
CUTOFF = "2026-10-24"


def run(conn):
    for table in ("connectors", "cards"):
        while True:
            with conn:
                n = conn.execute(f"DELETE FROM {table} WHERE id IN (SELECT id FROM {table} WHERE trashed_at < ? LIMIT 1000)",
                                 (CUTOFF,)).rowcount
            if not n:
                break
            if table == "cards":
                run.cards = getattr(run, "cards", 0) + n
    while True:
        with conn:
            n = conn.execute("""DELETE FROM frame_members WHERE rowid IN (SELECT rowid FROM frame_members
                WHERE frame_id NOT IN (SELECT id FROM cards) OR card_id NOT IN (SELECT id FROM cards) LIMIT 1000)""").rowcount
        if not n:
            break
    return getattr(run, "cards", 0)
