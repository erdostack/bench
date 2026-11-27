# collab-graph

The research office's coauthorship graph, Neo4j 5.26. One `Researcher` node per staff member (keyed by
ORCID, with their faculty) and one `COAUTHORED` relationship per pair of researchers who have published
together, with `papers` = how many papers they share.

Built every night: `etl/pairs.py` turns the publications export into pairs, `load/load_coauthors.cypher`
writes them.

The annual report to the funding council quotes, per faculty, the number of internal collaborations and
joint papers (`queries/collaboration_total.cypher`) and the collaborations with each other faculty
(`queries/cross_faculty_links.cypher`). Researchers see their own coauthors on the staff page
(`queries/my_coauthors.cypher`).
