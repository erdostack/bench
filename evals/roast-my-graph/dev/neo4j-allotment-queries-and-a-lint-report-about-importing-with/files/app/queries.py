"""Read queries for the plotkeeper web app."""

# site page header
SITE_SUMMARY = """
MATCH (s:Site {code: $site})
CALL {
  WITH s
  MATCH (s)-[:HAS_PLOT]->(p:Plot)
  RETURN count(p) AS plots,
         count(CASE WHEN NOT (p)<-[:TENANT_OF]-() THEN 1 END) AS free
}
CALL {
  WITH s
  MATCH (s)<-[:WAITING_FOR]-(a:Applicant)
  RETURN count(a) AS waiting
}
RETURN s.name, plots, free, waiting
"""

APPLICANT_OVERVIEW = """
MATCH (a:Applicant {ref: $ref})
CALL {
  WITH a
  OPTIONAL MATCH (a)-[w:WAITING_FOR]->(s:Site)
  RETURN collect({site: s.name, since: w.since}) AS lists
}
CALL {
  WITH a
  OPTIONAL MATCH (a)-[t:TENANT_OF]->(p:Plot)
  RETURN collect({plot: p.number, from: t.from}) AS plots
}
RETURN a.ref, a.name, lists, plots
"""

WAITING_LIST_POSITION = """
MATCH (a:Applicant {ref: $ref})-[w:WAITING_FOR]->(s:Site {code: $site})
CALL {
  WITH w, s
  MATCH (s)<-[other:WAITING_FOR]-(b:Applicant)
  WHERE other.since < w.since OR (other.since = w.since AND b.ref < $ref)
  RETURN count(b) AS ahead
}
RETURN ahead + 1 AS position
"""

FREE_PLOTS_BY_SITE = """
MATCH (s:Site)
CALL {
  WITH s
  MATCH (s)-[:HAS_PLOT]->(p:Plot)
  WHERE NOT (p)<-[:TENANT_OF]-()
  RETURN count(p) AS free
}
RETURN s.code, s.name, free
ORDER BY s.name
"""
