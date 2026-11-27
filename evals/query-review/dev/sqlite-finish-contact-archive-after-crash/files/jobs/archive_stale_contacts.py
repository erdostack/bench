"""Move contact edges unused since CUTOFF into contacts_archive."""
CUTOFF = "2025-11-01"     # bumped by hand each quarter
BATCH = 1000


def run(conn):
    moved = 0
    while True:
        keys = conn.execute(
            "SELECT owner_id, contact_id FROM contacts WHERE last_contact_at < ? ORDER BY rowid LIMIT ?",
            (CUTOFF, BATCH)).fetchall()
        if not keys:
            return moved
        with conn:
            conn.executemany("""
                INSERT INTO contacts_archive (owner_id, contact_id, created_at, last_contact_at, archived_at)
                SELECT owner_id, contact_id, created_at, last_contact_at, datetime('now')
                FROM contacts WHERE owner_id = ? AND contact_id = ?""", keys)
        with conn:
            conn.executemany("DELETE FROM contacts WHERE owner_id = ? AND contact_id = ?", keys)
        moved += len(keys)
