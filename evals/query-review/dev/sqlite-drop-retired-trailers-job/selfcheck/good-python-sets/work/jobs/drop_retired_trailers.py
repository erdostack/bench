def run(conn):
    coupled = {r[0] for r in conn.execute("SELECT DISTINCT trailer_id FROM coupling")}
    named = {r[0] for r in conn.execute("SELECT DISTINCT asset_no FROM inspection")}
    ids = [i for i, no in conn.execute(
        "SELECT id, trailer_no FROM trailer WHERE status = 'retired' AND date(retired_on) < date('2025-01-01')")
        if i not in coupled and no not in named]
    for k in range(0, len(ids), 500):
        part = ids[k:k + 500]
        conn.execute(f"DELETE FROM trailer WHERE id IN ({','.join('?' * len(part))})", part)
        conn.commit()
    return len(ids)
