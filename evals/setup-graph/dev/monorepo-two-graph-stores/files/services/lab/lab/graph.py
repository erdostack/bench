"""The lab's embedded snapshot."""
import kuzu

PATH = "var/baskets.kz"


def connect(read_only: bool = True) -> kuzu.Connection:
    return kuzu.Connection(kuzu.Database(PATH, read_only=read_only))
