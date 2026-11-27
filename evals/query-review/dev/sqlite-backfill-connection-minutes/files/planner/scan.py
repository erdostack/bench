"""Earliest arrival by connection scan (RP-311 moves the comparisons to dep_min / arr_min)."""


def earliest_arrival(conn, origin, destination, depart_after):
    best = {origin: depart_after}
    for dep, arr, a, b in conn.execute(
            "SELECT dep, arr, from_station, to_station FROM connections WHERE dep >= ? ORDER BY dep, id", (depart_after,)):
        if a in best and best[a] <= dep and arr < best.get(b, "99:99"):
            best[b] = arr
    return best.get(destination)
