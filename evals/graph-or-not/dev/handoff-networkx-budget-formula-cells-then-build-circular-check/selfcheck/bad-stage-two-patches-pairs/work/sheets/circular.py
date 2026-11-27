def circular_cells(conn):
    rows = conn.execute(
        "SELECT c.sheet, c.ref, d.sheet, d.ref FROM reference r "
        "JOIN cell c ON c.id = r.cell_id JOIN cell d ON d.id = r.depends_on")
    edges = {(f"{s1}!{r1}", f"{s2}!{r2}") for s1, r1, s2, r2 in rows}
    flagged = set()
    for a, b in edges:
        if (b, a) in edges or a == b:
            flagged.update((a, b))
    return sorted(flagged)
