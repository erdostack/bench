"""0058 (CONF-212): archive scheduled 2025 sessions; cancelled stay cancelled. Safe to re-apply."""

def run(conn):
    archived = 0
    while True:
        with conn:
            n = conn.execute("UPDATE nodes SET status = 'archived' WHERE id IN (SELECT id FROM nodes WHERE kind = 'session' AND status = 'scheduled' AND starts_at < '2026-01-01' LIMIT 10)").rowcount
        if not n:
            return archived
        archived += n
