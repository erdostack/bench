"""Recalculation after an edit. Called by the doc server with the workbook's SQLite file already open."""
from . import engine


def on_edit(conn, sheet, addr):
    # TODO: this recalculates every formula in the workbook on every edit. Fine for a few hundred cells, far too
    #       slow on the finance models. Recalculate only the cells that depend on (sheet, addr).
    rows = conn.execute("SELECT sheet, addr FROM cell WHERE formula IS NOT NULL").fetchall()
    for s, a in rows:
        engine.evaluate(conn, s, a)
