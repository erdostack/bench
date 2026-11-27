# Roast: opsmap queries

Six queries. One of them asks the graph a question it has been carefully built to answer with silence, and one does a headcount of the entire data centre 600 times a second. The other four are fine, which only makes these two look worse.

## Findings

### 1. services_on_host (critical)

**Problem.** The arrow points from the host to the service. Everything else in the repo says the opposite: docs/model.md lists RUNS_ON as going from Service to Host, upsert_instances writes (s)-[:RUNS_ON]->(h), and owners_to_page reads it that way round. So this query matches nothing and returns an empty list for every host, which the incident bot will report as "no services affected" during an outage.

**Fix.** Turn the arrow round: MATCH (h:Host {name: $host})<-[:RUNS_ON]-(s:Service) RETURN s.name AS service, s.tier AS tier ORDER BY s.tier.

### 2. host_by_serial (high)

**Problem.** It finds a host by its serial, and nothing in constraints.cypher covers Host.serial; the only thing declared for Host is the uniqueness of name. Without help the database has to look at all 410,000 hosts to find one, and this is the query that runs 600 times a second.

**Fix.** Declare it: CREATE CONSTRAINT host_serial IF NOT EXISTS FOR (h:Host) REQUIRE h.serial IS UNIQUE; if serials are unique (they should be), otherwise CREATE INDEX host_serial IF NOT EXISTS FOR (h:Host) ON (h.serial);

The other four queries agree with the model and start from a keyed property.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
