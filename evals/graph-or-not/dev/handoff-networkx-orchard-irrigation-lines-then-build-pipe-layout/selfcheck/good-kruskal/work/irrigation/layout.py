def pipe_layout(conn):
    runs = sorted((length + 40 * crosses, a, b)
                  for a, b, length, crosses in conn.execute("SELECT a, b, length_m, crosses_track FROM candidate_run"))
    parent = {v: v for (v,) in conn.execute("SELECT id FROM valve")}

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    out = []
    for _, a, b in runs:
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[ra] = rb
            out.append((a, b))
    return out
