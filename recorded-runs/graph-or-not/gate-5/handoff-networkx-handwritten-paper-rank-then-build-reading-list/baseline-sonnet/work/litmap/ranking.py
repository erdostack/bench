"""Reading list ranking: the k highest-ranked papers by PageRank importance."""
from litmap.score import importance


def reading_list(conn, k):
    """Return the ids of the k highest-ranked papers, best first (ties broken by lower id)."""
    s = importance(conn)
    return sorted(s, key=lambda p: (-s[p], p))[:k]
