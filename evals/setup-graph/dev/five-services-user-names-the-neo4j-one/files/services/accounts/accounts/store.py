import os

import psycopg

DSN = os.environ.get("ACCOUNTS_DSN", "postgresql://postgres@localhost:5432/accounts")


def invoices_for(customer_id: int) -> list[dict]:
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, issued_on, total_cents FROM invoice WHERE customer_id = %s ORDER BY issued_on", (customer_id,))
        return [{"id": r[0], "issued_on": r[1].isoformat(), "total_cents": r[2]} for r in cur.fetchall()]
