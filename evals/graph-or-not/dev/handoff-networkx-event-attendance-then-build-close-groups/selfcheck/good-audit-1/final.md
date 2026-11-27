Added seminar/groups.py. close_groups(conn) follows docs/graph/DECISION.md: two women are close when they went to
at least 4 events together, and the groups are the connected components of those ties. Women with no close tie are
left out.
