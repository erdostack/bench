"""Nightly scores job: reach and ring for every account (docs/scores.md).

Muted follows: no reach, but they still join rings (trust & safety, see docs/graph/DECISION.md).
Run from cron after the export lands: python3 -m jobs.nightly_scores exports/
"""
import sys
from pathlib import Path

D, STEPS = 0.85, 20


def _rows(path):
    """Yield dicts keyed by the column names in the '# ...' header line."""
    cols = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                if cols is None:
                    cols = line.lstrip("#").split("(")[0].split()
                continue
            if line.strip():
                yield dict(zip(cols, line.split()))


def scores(export_dir):
    d = Path(export_dir)
    accounts = [int(r["account_id"]) for r in _rows(d / "accounts.txt")]
    links = [(int(r["follower_id"]), int(r["followed_id"]), r["muted"] == "1") for r in _rows(d / "follows.edges")]

    # rings: union-find over every follow; the ring id is the smallest account id in the ring
    up = {a: a for a in accounts}

    def root(a):
        while up[a] != a:
            up[a] = up[up[a]]
            a = up[a]
        return a
    for a, b, _ in links:
        ra, rb = root(a), root(b)
        if ra != rb:
            up[max(ra, rb)] = min(ra, rb)

    # reach: 20 steps over the follows that are not muted
    n = len(accounts)
    live = [(a, b) for a, b, muted in links if not muted]
    following = dict.fromkeys(accounts, 0)
    for a, _ in live:
        following[a] += 1
    rank = dict.fromkeys(accounts, 1.0 / n)
    for _ in range(STEPS):
        spill = D * sum(rank[a] for a in accounts if not any(x == a for x, _, _ in links)) / n   # follows nobody at all
        nxt = dict.fromkeys(accounts, (1 - D) / n + spill)
        for a, b in live:
            nxt[b] += D * rank[a] / following[a]
        rank = nxt
    return {a: (root(a), rank[a]) for a in accounts}


if __name__ == "__main__":
    print(len(scores(sys.argv[1] if len(sys.argv) > 1 else "exports")), "accounts scored")
