"""0032: delete offers that expired before 2026-11-01 (the trade window's offer lookup times out on them).
Expired offers are history only (docs/trading.md). Commits 2,000 rows at a time (limit 2,500);
safe to apply again if it stops part-way.
Apply with: bin/apply bazaar changes/0032_delete_offers_expired_before_november.py"""
CUTOFF = "2026-11-01"
CHUNK = 2000


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'offer' "
                "AND (status = 'expired' OR expires_at < ?) LIMIT ?)", (CUTOFF, CHUNK)).rowcount
        if not n:
            return removed
        removed += n
