"""Which records are the same person."""


def group_records(conn):
    group_of = {}
    groups = []
    first_with = {}
    rows = conn.execute("SELECT record_id, kind, value FROM contact_point WHERE kind != 'address' ORDER BY record_id, kind, value")
    for record_id, kind, value in rows:
        key = (kind, value)
        if key in first_with:
            g = group_of[first_with[key]]
            if record_id not in group_of:
                group_of[record_id] = g
                groups[g].append(record_id)
        else:
            first_with[key] = record_id
            if record_id not in group_of:
                group_of[record_id] = len(groups)
                groups.append([record_id])
    for (rid,) in conn.execute("SELECT id FROM record ORDER BY id"):
        if rid not in group_of:
            groups.append([rid])
    return [sorted(g) for g in groups]
