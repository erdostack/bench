def critical_stops(conn):
    rows = conn.execute("SELECT code FROM stop ORDER BY boardings_per_day DESC LIMIT 15")
    return sorted(code for (code,) in rows)
