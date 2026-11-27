from sheets.circular import circular_cells


def on_save(conn):
    """Called by the editor after every edit; the editor shows the returned warnings."""
    return {"circular": circular_cells(conn)}
