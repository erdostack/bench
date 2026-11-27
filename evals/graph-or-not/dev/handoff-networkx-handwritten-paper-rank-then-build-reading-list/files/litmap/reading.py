"""The "start here" reading list."""
from litmap.score import importance


def start_here(conn, k=20):
    s = importance(conn)
    # TODO: switch the reading list to the ranking we decide on
    return sorted(s, key=s.get, reverse=True)[:k]
