"""Which trees have no compatible partner within reach?"""
from .db import read

LONELY = """
MATCH (t:Tree)-[:OF_VARIETY]->(v:Variety)
WHERE NOT EXISTS {
  MATCH (t)-[:IN_ROW]->(:Row)-[:ADJACENT_TO*0..2]-(:Row)<-[:IN_ROW]-(other:Tree)-[:OF_VARIETY]->(p:Variety)
  WHERE (v)-[:POLLINATED_BY]->(p)
}
RETURN t.tag AS tree, v.name AS variety
ORDER BY variety, tree
"""


def without_partner() -> list[dict]:
    return read(LONELY)
