"""Rebuild COAUTHORED from the publication list: one relationship per unordered pair."""

LINK_PAIR = """
UNWIND $pairs AS pair
MATCH (a:Researcher {id: pair.lo}), (b:Researcher {id: pair.hi})
MERGE (a)-[c:COAUTHORED]->(b)
SET c.papers = pair.papers
"""


def pairs_from_papers(papers):
    """papers: iterable of author-id lists. Returns one dict per unordered pair, lower id first."""
    counts = {}
    for authors in papers:
        ids = sorted(set(authors))
        for i, lo in enumerate(ids):
            for hi in ids[i + 1:]:
                counts[(lo, hi)] = counts.get((lo, hi), 0) + 1
    return [{"lo": lo, "hi": hi, "papers": n} for (lo, hi), n in sorted(counts.items())]


def link(session, papers, batch=5000):
    pairs = pairs_from_papers(papers)
    for start in range(0, len(pairs), batch):
        chunk = pairs[start:start + batch]
        session.execute_write(lambda tx: tx.run(LINK_PAIR, pairs=chunk).consume())
