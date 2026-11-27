"""Promote the referees who passed the October 2026 clinic from grade C to B."""
PASSED = (118, 204, 233, 307)


def run(conn):
    with conn:
        return conn.execute(f"UPDATE referees SET grade = 'B' WHERE grade = 'C' AND id IN ({','.join('?' * len(PASSED))})",
                            PASSED).rowcount
