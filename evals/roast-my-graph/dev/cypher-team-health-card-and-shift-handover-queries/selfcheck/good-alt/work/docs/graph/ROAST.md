# Roast: pagerline team page queries

team_health returns members times incidents for both counts. Aggregate members with WITH before
matching incidents. Everything else is fine.

## Findings

### 1. queries/cards.cypher: team_health card (high)

**Problem.** members and incidents_90d come out as the product of the two: there is nothing linking the Person rows to the Incident rows, so the aggregation sees one row per (person, incident) pair.

**Fix.** Aggregate the members first: MATCH (p:Person)-[:MEMBER_OF]->(t:Team {id: $team}) WITH t, count(p) AS members MATCH (i:Incident)-[:ASSIGNED_TO]->(t) WHERE i.opened_at >= datetime() - duration('P90D') RETURN members, count(i) AS incidents_90d, count(CASE WHEN i.severity = 'sev1' THEN 1 END) AS sev1_90d (and handle a team with no recent incidents with OPTIONAL MATCH).

### 2. Incident.opened_at (low)

**Problem.** open_incidents filters on closed_at after expanding the team's incidents; fine at 160,000 in the graph.

**Fix.** No change.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
