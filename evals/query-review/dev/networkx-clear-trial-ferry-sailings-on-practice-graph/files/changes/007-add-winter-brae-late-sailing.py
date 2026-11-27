"""007: winter timetable 2026-27: a 21:30 Brae to Dunvar sailing on Fridays in December, on MV Selvay.
Reviewed: h.mackinnon. Applied to live 2026-11-02."""
from datetime import date, timedelta


def run(G):
    d, added = date(2026, 12, 4), 0
    while d.month == 12:
        s = f"S-{d:%Y%m%d}-2130-BRAE"
        G.add_node(s, kind="sailing", day=d.isoformat(), departs="21:30")
        G.add_edge(s, "PORT-BRAE", kind="departs")
        G.add_edge(s, "PORT-DUNVAR", kind="arrives")
        G.add_edge(s, "MV-SELVAY", kind="operated_by")
        d += timedelta(days=7)
        added += 1
    return added
