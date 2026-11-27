def shared_events(conn, a, b):
    rows = conn.execute(
        "SELECT e.label FROM attended x JOIN woman wa ON wa.id = x.woman_id "
        "JOIN attended y ON y.event_id = x.event_id JOIN woman wb ON wb.id = y.woman_id "
        "JOIN event e ON e.id = x.event_id WHERE wa.name = ? AND wb.name = ? ORDER BY e.id", (a, b))
    return [label for (label,) in rows]
