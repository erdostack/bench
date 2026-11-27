"""Move contact edges unused since CUTOFF into contacts_archive.

Each batch is copied and deleted in the same transaction, and the copy skips edges that are already in
the archive (left there by a run that died between copy and delete before this was fixed), so a run that
dies is safe to repeat."""
CUTOFF = "2025-11-01"     # bumped by hand each quarter
BATCH = 500               # 500 copied + 500 deleted = 1,000 changed rows per transaction


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
                SELECT c.owner_id, c.contact_id, c.created_at, c.last_contact_at, datetime('now')
                FROM contacts c
                WHERE c.owner_id = ? AND c.contact_id = ?
                  AND NOT EXISTS (SELECT 1 FROM contacts_archive a
                                  WHERE a.owner_id = c.owner_id AND a.contact_id = c.contact_id
                                    AND a.created_at = c.created_at AND a.last_contact_at = c.last_contact_at)""", keys)
            conn.executemany("DELETE FROM contacts WHERE owner_id = ? AND contact_id = ?", keys)
        moved += len(keys)
