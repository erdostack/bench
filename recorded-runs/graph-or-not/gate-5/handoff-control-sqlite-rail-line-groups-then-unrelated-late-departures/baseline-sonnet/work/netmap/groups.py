"""Colour groups for the printed map: lines that connect, directly or through other lines, share a colour family."""


def line_groups(conn):
    """Return {line_id: family} where lines sharing a station, directly or through other lines, share a family.

    Families are numbered from 1 in order of their lowest line_id, so the result is stable between runs.
    A line with no stations is a family of its own.
    """
    parent = {line_id: line_id for (line_id,) in conn.execute("SELECT line_id FROM line")}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    first_line_at = {}
    for line_id, station in conn.execute("SELECT line_id, station_code FROM line_station"):
        other = first_line_at.setdefault(station, line_id)
        a, b = find(line_id), find(other)
        if a != b:
            parent[max(a, b)] = min(a, b)

    family_of_root = {}
    groups = {}
    for line_id in sorted(parent):
        root = find(line_id)
        groups[line_id] = family_of_root.setdefault(root, len(family_of_root) + 1)
    return groups
