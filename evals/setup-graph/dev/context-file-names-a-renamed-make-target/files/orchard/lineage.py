"""Where does a tree's scion wood come from?"""
from .db import read

ANCESTRY = """
MATCH (t:Tree {tag: $tag})-[:SCION_FROM*1..10]->(source:Tree)
RETURN source.tag AS tag, source.planted AS planted
ORDER BY planted
"""


def ancestry(tag: str) -> list[dict]:
    return read(ANCESTRY, tag=tag)
