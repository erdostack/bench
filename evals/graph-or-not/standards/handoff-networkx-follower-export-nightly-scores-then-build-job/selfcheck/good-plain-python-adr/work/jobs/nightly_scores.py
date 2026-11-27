"""Nightly scores job: reach and ring for every account (docs/scores.md, docs/adr/0003)."""
from collections import defaultdict
from pathlib import Path


def _rows(path):
    with open(path) as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                yield line.split()


def scores(export_dir, steps=20, d=0.85):
    root = Path(export_dir)
    accounts = [int(r[0]) for r in _rows(root / "accounts.txt")]
    follows = [(int(b), int(a), m == "1") for a, b, m in _rows(root / "follows.edges")]  # (follower, followed, muted)
    parent = {a: a for a in accounts}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v, _ in follows:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[max(ru, rv)] = min(ru, rv)
    n = len(accounts)
    following = defaultdict(int)
    followers = defaultdict(list)
    for u, v, muted in follows:
        if not muted:
            following[u] += 1
            followers[v].append(u)
    r = {a: 1 / n for a in accounts}
    for _ in range(steps):
        spill = d * sum(r[a] for a in accounts if not following[a]) / n
        r = {a: (1 - d) / n + spill + d * sum(r[u] / following[u] for u in followers[a]) for a in accounts}
    return {a: {"ring": find(a), "reach": r[a]} for a in accounts}
