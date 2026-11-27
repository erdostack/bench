"""MON-14: set ad_slots.cpm_cents to cpm rounded to the nearest cent, 1,000 rows at a time.

The first run truncated (CAST(cpm * 100 AS INTEGER) turns 0.29 into 28), so rows it filled can be a cent
short. Every row whose cpm_cents is NULL or not the rounded price is (re)written; re-running is harmless."""

BATCH = 1000
RIGHT = "CAST(ROUND(cpm * 100) AS INTEGER)"


def run(conn, start_id=0):
    done = 0
    while True:
        with conn:
            n = conn.execute(f"""UPDATE ad_slots SET cpm_cents = {RIGHT} WHERE id IN (
                                   SELECT id FROM ad_slots WHERE id > ? AND (cpm_cents IS NULL OR cpm_cents <> {RIGHT})
                                   ORDER BY id LIMIT ?)""", (int(start_id), BATCH)).rowcount
        done += n
        if not n:
            return done
