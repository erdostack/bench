def run(conn, start_id=0):
    with conn:
        return conn.execute("UPDATE ad_slots SET cpm_cents = CAST(ROUND(cpm * 100) AS INTEGER)").rowcount
