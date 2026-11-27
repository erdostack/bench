"""0032 (HB-58): Hollin Moor (AP-17) closes; its active colonies move to Moor End (AP-22).
Colonies under standstill stay at AP-17 (docs/movements.md). 100 rows per transaction; safe to apply again."""
def run(conn):
    with conn:
        return conn.execute(
            "UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'AP-22') WHERE kind = 'kept_at' "
            "AND dst = (SELECT id FROM nodes WHERE code = 'AP-17') "
            "AND src IN (SELECT id FROM nodes WHERE status = 'active')").rowcount
