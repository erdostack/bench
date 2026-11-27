"""MILK-212: backfill ships_to edges for 2025 and 2026 from the collection tickets, 50 farms at a time.

Resumes after the last farm recorded in job_state.
python -m jobs backfill_ships_to"""
CHUNK = 50
JOB = "backfill_ships_to"

INSERT = """
INSERT INTO edges (src, dst, kind, year, litres)
SELECT farm_id, plant_id, 'ships_to', CAST(substr(day, 1, 4) AS INTEGER), SUM(litres)
FROM tickets
WHERE farm_id IN ({ids}) AND day >= '2025-01-01'
  AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src = tickets.farm_id AND e.dst = tickets.plant_id AND e.kind = 'ships_to')
GROUP BY farm_id, plant_id, substr(day, 1, 4)
"""


def run(conn):
    row = conn.execute("SELECT last_farm FROM job_state WHERE job = ?", (JOB,)).fetchone()
    start = row[0] if row else 0
    farms = [r[0] for r in conn.execute("SELECT id FROM nodes WHERE kind = 'farm' AND id > ? ORDER BY id", (start,))]
    written = 0
    for i in range(0, len(farms), CHUNK):
        part = farms[i:i + CHUNK]
        with conn:
            written += conn.execute(INSERT.format(ids=",".join("?" * len(part))), part).rowcount
        with conn:
            conn.execute("INSERT INTO job_state VALUES (?, ?) ON CONFLICT (job) DO UPDATE SET last_farm = excluded.last_farm",
                         (JOB, part[-1]))
    return written
