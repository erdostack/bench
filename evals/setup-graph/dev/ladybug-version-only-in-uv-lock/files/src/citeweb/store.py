"""The embedded database. Opened read-only unless the loader asks otherwise."""
import os

import ladybug as lb

PATH = os.environ.get("CITEWEB_DB", "var/citeweb.lbug")


def connect(read_only: bool = True) -> "lb.Connection":
    return lb.Connection(lb.Database(PATH, read_only=read_only))
