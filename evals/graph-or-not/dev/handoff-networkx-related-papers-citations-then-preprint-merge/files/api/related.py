"""Related papers: within three citation hops, either direction."""
from collections import Counter


def related(cur, paper_id, limit=20):
    paths = Counter({paper_id: 1})
    frontier = Counter({paper_id: 1})
    for _ in range(3):
        ids = list(frontier)
        cur.execute("SELECT citing, cited FROM citation WHERE citing = ANY(%s) OR cited = ANY(%s)", (ids, ids))
        nxt = Counter()
        for citing, cited in cur.fetchall():
            for here, there in ((citing, cited), (cited, citing)):
                if here in frontier:
                    nxt[there] += frontier[here]
        paths.update(nxt)
        frontier = nxt
    del paths[paper_id]
    return [p for p, _ in paths.most_common(limit)]
