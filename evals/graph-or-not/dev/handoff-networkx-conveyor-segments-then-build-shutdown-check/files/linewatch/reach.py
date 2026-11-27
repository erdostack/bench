"""Which stations can be reached from a station. Started for the shutdown check; not used yet."""


def neighbours(conn, station_id):
    rows = conn.execute(
        "SELECT to_station FROM segment WHERE from_station = ? UNION SELECT from_station FROM segment WHERE to_station = ?",
        (station_id, station_id)).fetchall()
    return [r[0] for r in rows]


def reachable(conn, start):
    seen, todo = {start}, [start]
    while todo:
        for n in neighbours(conn, todo.pop()):
            if n not in seen:
                seen.add(n)
                todo.append(n)
    return seen
