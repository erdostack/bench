"""Opening the database. Everything else goes through connect()."""
import os
from pathlib import Path

import real_ladybug as lb

PATH = os.environ.get("BANDTREE_DB", str(Path(__file__).resolve().parent.parent / "var" / "bandtree.lbug"))


def connect(read_only: bool = True) -> "lb.Connection":
    return lb.Connection(lb.Database(PATH, read_only=read_only))
