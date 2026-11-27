"""MILK-212: backfill ships_to edges for 2025 and 2026, keyed on (farm, plant, kind, year) so a rerun is a no-op."""
CHUNK = 50


def run(conn):
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS edges_ships_to_key ON edges (src, dst, kind, year) WHERE kind = 'ships_to'")
    conn.commit()
    farms = [r[0] for r in conn.execute("SELECT id FROM nodes WHERE kind = 'farm' ORDER BY id")]
    written = 0
    for i in range(0, len(farms), CHUNK):
        part = farms[i:i + CHUNK]
        with conn:
            written += conn.execute(
                "INSERT INTO edges (src, dst, kind, year, litres) "
                "SELECT farm_id, plant_id, 'ships_to', CAST(substr(day, 1, 4) AS INTEGER), SUM(litres) FROM tickets "
                f"WHERE farm_id IN ({','.join('?' * len(part))}) AND day >= '2025-01-01' "
                "GROUP BY farm_id, plant_id, substr(day, 1, 4) "
                "ON CONFLICT (src, dst, kind, year) WHERE kind = 'ships_to' DO NOTHING", part).rowcount
    return written
