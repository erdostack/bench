"""Which trench runs to dig so that every valve is fed from the pump."""


def pipe_layout(conn):
    """Return the runs to dig as (a, b) pairs.

    Start at the pump and keep going to the nearest valve not yet connected.
    """
    runs = {}
    for a, b, length, _ in conn.execute("SELECT a, b, length_m, crosses_track FROM candidate_run"):
        runs[(a, b)] = runs[(b, a)] = length
    valves = {v for (v,) in conn.execute("SELECT id FROM valve")}
    done, current, out = {0}, 0, []
    while len(done) < len(valves):
        options = [(runs[(current, v)], current, v) for v in valves - done if (current, v) in runs]
        if not options:   # dead end: continue from the nearest connected valve
            options = [(runs[(u, v)], u, v) for u in done for v in valves - done if (u, v) in runs]
        if not options:
            raise ValueError("some valves cannot be reached")
        _, u, v = min(options)
        out.append((u, v))
        done.add(v)
        current = v
    return out
