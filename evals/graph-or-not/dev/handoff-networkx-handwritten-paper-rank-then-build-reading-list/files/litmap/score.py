"""Importance score for the reading list (written by a student in 2023)."""
from collections import defaultdict


def importance(conn, rounds=10, damping=0.85):
    papers = [i for (i,) in conn.execute("SELECT id FROM paper")]
    refs = defaultdict(list)
    for citing, cited in conn.execute("SELECT citing_id, cited_id FROM cites"):
        refs[citing].append(cited)
    n = len(papers)
    score = {p: 1.0 / n for p in papers}
    for _ in range(rounds):
        new = {p: (1 - damping) / n for p in papers}
        for p in papers:
            for q in refs[p]:
                new[q] += damping * score[p] / len(refs[p])
        score = new
    return score
