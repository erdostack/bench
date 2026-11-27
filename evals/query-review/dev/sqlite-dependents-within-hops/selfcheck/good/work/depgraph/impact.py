"""Who is affected by a change to a package."""


def direct_dependents(conn, package_id):
    """Ids of the packages that declare a dependency on `package_id`, ascending."""
    rows = conn.execute(
        "SELECT package_id FROM depends_on WHERE dependency_id = ? ORDER BY package_id",
        (package_id,),
    )
    return [r[0] for r in rows]


def dependents_within(conn, package_id, max_hops):
    """(package_id, hops) for every package that depends on `package_id` within `max_hops` levels.

    hops is the smallest number of levels. Sorted by hops, then package_id; the package itself is left out.
    UNION (not UNION ALL) matters: the graph has cycles through platform-base, and without dedup the
    recursion enumerates every walk instead of every package.
    """
    rows = conn.execute(
        """
        WITH RECURSIVE up(id, hops) AS (
            SELECT package_id, 1 FROM depends_on WHERE dependency_id = :pkg
            UNION
            SELECT d.package_id, up.hops + 1
            FROM up
            JOIN depends_on d ON d.dependency_id = up.id
            WHERE up.hops < :max_hops
        )
        SELECT id, min(hops) AS hops
        FROM up
        WHERE id <> :pkg
        GROUP BY id
        ORDER BY hops, id
        """,
        {"pkg": package_id, "max_hops": max_hops},
    )
    return [(r[0], r[1]) for r in rows]
