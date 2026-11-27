"""Route questions asked by the dispatch desk."""
from .graph import rows

# Breadth-first expansion over legs that are not closed; the lambda filters every hop.
FEWEST_LEGS = """
MATCH p = (a:Depot {code: $src})-[:LEG *BFS ..8 (e, n | NOT e.closed)]->(b:Depot {code: $dst})
RETURN [d IN nodes(p) | d.code] AS depots, size(relationships(p)) AS legs
"""


def fewest_legs(src: str, dst: str) -> dict | None:
    found = rows(FEWEST_LEGS, src=src, dst=dst)
    return found[0] if found else None
