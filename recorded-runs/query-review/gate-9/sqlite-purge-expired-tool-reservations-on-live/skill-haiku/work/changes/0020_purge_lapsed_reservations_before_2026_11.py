"""0020: purge reservations that lapsed before 2026-11-01 (docs/reservations.md). The counter app still shows
these holds. Commits at most 1,000 rows per transaction (docs/targets.md) and carries on until none are left,
so an apply that stops part-way can simply be run again and changes nothing once done. Loans and kits are
not touched. Not yet applied: to be applied to live by the systems volunteer after review."""


def run(conn):
    total = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM edges WHERE id IN (SELECT id FROM edges "
                "WHERE kind = 'reservation' AND ends_on < '2026-11-01' LIMIT 1000)"
            ).rowcount
        if n == 0:
            return total
        total += n
