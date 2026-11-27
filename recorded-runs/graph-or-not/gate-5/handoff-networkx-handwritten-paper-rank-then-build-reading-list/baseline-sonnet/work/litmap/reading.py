"""The "start here" reading list."""
from litmap.ranking import reading_list


def start_here(conn, k=20):
    return reading_list(conn, k)
