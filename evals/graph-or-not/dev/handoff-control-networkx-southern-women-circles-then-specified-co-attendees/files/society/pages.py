"""Exhibit pages (rendering only)."""
from society.data import load_attendance, women


def index_page():
    return {"women": women()}


def woman_page(name):
    return {"name": name, "events": sorted(e for w, e in load_attendance() if w == name)}

# TODO: "circles" page: pick a woman and show who she was connected to through the events, step by step.
