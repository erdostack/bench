"""0020 (STK-131): Hunslet (ST-HUN) closes on Friday; its fixtures move to Stourton (ST-STO) (docs/stores.md).
Moves only stored_at edges; works_at (HR) and serves (transport) are left alone. 1,000 rows a commit;
safe to apply again."""


def run(conn):
    moved = 0
    while True:
        with conn:
            n = conn.execute(
                "UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'ST-STO') WHERE id IN ("
                "SELECT id FROM edges WHERE kind = 'stored_at' "
                "AND dst = (SELECT id FROM nodes WHERE code = 'ST-HUN') LIMIT 2000)").rowcount
        if not n:
            return moved
        moved += n
