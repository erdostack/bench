"""Reachability between families over marriage ties."""


def families_within(conn, family, k):
    """Sorted list of the other families reachable from `family` through at most `k` marriage ties.

    A tie joins two families in either direction. `family` itself is never in the result; the list is
    empty when nothing is reachable (including k = 0, a negative k, or a family with no ties).
    """
    seen = {family}
    frontier = {family}
    for _ in range(max(k, 0)):
        if not frontier:
            break
        marks = ",".join("?" * len(frontier))
        args = tuple(frontier)
        rows = conn.execute(
            f"SELECT family_a, family_b FROM marriage_tie "
            f"WHERE family_a IN ({marks}) OR family_b IN ({marks})",
            args + args,
        )
        nxt = {f for row in rows for f in row} - seen
        seen |= nxt
        frontier = nxt
    return sorted(seen - {family})
