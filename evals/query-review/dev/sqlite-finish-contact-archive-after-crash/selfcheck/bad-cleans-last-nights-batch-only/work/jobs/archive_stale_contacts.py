"""Move contact edges unused since CUTOFF into contacts_archive."""
CUTOFF = "2025-11-01"     # bumped by hand each quarter
BATCH = 1000


def run(conn):
    # one-off: the 2026-11-22 run died after copying batch 42; drop those from contacts first
    with conn:
        moved = conn.execute("""DELETE FROM contacts WHERE EXISTS (
            SELECT 1 FROM contacts_archive a WHERE a.owner_id = contacts.owner_id AND a.contact_id = contacts.contact_id
            AND a.archived_at LIKE '2026-11-22%')""").rowcount
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
