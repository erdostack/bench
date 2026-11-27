"""Nightly: rebuild NEAR between depots within 80 km."""
REBUILD = """
MATCH (:Depot)-[n:NEAR]->(:Depot) DELETE n
WITH count(*) AS _
MATCH (a:Depot), (b:Depot)
WHERE a <> b AND point.distance(a.location, b.location) < 80000
CREATE (a)-[:NEAR {km: round(point.distance(a.location, b.location) / 1000)}]->(b)
"""
