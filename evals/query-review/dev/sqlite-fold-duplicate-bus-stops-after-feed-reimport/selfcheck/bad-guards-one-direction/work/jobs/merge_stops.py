def run(conn):
    pairs = conn.execute("SELECT dup_id, keep_id FROM stop_merge").fetchall()
    with conn:
        for dup, keep in pairs:
            conn.execute("INSERT OR IGNORE INTO edge SELECT ?, dst, rel, route FROM edge WHERE src = ? AND dst <> ?", (keep, dup, keep))
            conn.execute("INSERT OR IGNORE INTO edge SELECT src, ?, rel, route FROM edge WHERE dst = ?", (keep, dup))
            conn.execute("DELETE FROM edge WHERE src = ? OR dst = ?", (dup, dup))
            conn.execute("DELETE FROM node WHERE id = ?", (dup,))
    return len(pairs)
