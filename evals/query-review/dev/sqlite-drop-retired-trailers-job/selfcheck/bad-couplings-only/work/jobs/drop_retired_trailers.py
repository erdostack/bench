def run(conn):
    cur = conn.execute("""DELETE FROM trailer WHERE status = 'retired' AND retired_on < '2025-01-01'
                           AND id NOT IN (SELECT trailer_id FROM coupling)""")
    conn.commit()
    return cur.rowcount
