"""Who is affected by a change to a package."""


def direct_dependents(conn, package_id):
    """Ids of the packages that declare a dependency on `package_id`, ascending."""
    rows = conn.execute(
        "SELECT package_id FROM depends_on WHERE dependency_id = ? ORDER BY package_id",
        (package_id,),
    )
    return [r[0] for r in rows]
