"""Open the embedded database. One Database per process, a Connection per caller."""
import os
from functools import lru_cache

import kuzu


@lru_cache(maxsize=1)
def database(read_only: bool = True) -> "kuzu.Database":
    return kuzu.Database(os.environ.get("PANTRY_DB", "./var/pantry.kz"), read_only=read_only)


def connect(read_only: bool = True) -> "kuzu.Connection":
    return kuzu.Connection(database(read_only))
