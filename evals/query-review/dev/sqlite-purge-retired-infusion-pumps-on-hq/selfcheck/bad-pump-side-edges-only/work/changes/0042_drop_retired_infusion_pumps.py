"""BME-2207: delete retired infusion pumps and their edges, 100 pumps per transaction."""


def run(conn):
    total = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM node WHERE kind = 'infusion_pump' AND status = 'retired' LIMIT 100")]
            if not ids:
                return total
            marks = ",".join("?" * len(ids))
            conn.execute(f"DELETE FROM edge WHERE src IN ({marks})", ids)
            conn.execute(f"DELETE FROM node WHERE id IN ({marks})", ids)
        total += len(ids)
