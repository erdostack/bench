"""Circuit trace: everything a pin reaches through wires and splices."""


def trace(cur, endpoint_id):
    seen, todo = {endpoint_id}, [endpoint_id]
    while todo:
        ep = todo.pop()
        cur.execute("SELECT to_ep FROM wire WHERE from_ep = %s UNION SELECT from_ep FROM wire WHERE to_ep = %s",
                    (ep, ep))
        for (nxt,) in cur.fetchall():
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return sorted(seen)
