"""Move contact edges unused since CUTOFF into contacts_archive, all in one transaction."""
CUTOFF = "2025-11-01"


def run(conn):
    with conn:
        conn.execute("""
            INSERT INTO contacts_archive
            SELECT c.owner_id, c.contact_id, c.created_at, c.last_contact_at, datetime('now') FROM contacts c
            WHERE c.last_contact_at < ? AND NOT EXISTS (SELECT 1 FROM contacts_archive a
                WHERE a.owner_id = c.owner_id AND a.contact_id = c.contact_id AND a.created_at = c.created_at)""", (CUTOFF,))
        return conn.execute("DELETE FROM contacts WHERE last_contact_at < ?", (CUTOFF,)).rowcount
