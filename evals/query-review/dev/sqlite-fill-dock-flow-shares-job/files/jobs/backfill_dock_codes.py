"""Give every dock without a code its 'DK-nnnn' code (migration 0005)."""
BATCH = 2000


def run(conn):
    filled = 0
    while True:
        with conn:
            n = conn.execute(
                "UPDATE docks SET code = printf('DK-%04d', id) "
                "WHERE id IN (SELECT id FROM docks WHERE code IS NULL LIMIT ?)", (BATCH,)).rowcount
        if n == 0:
            return filled
        filled += n
