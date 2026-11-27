// name: freelancers_with_skill
MATCH (s:Skill {name: $skill})<-[:FOR_SKILL]-(c:SkillClaim)<-[:CLAIMS]-(f:Freelancer)-[:LIVES_IN]->(city:City)
WHERE c.level >= $min_level AND ($city IS NULL OR city.name = $city)
RETURN f.id, f.display_name, c.level, c.since, city.name
ORDER BY c.level DESC, c.since
LIMIT 50;

// name: freelancer_profile
MATCH (f:Freelancer {id: $id})
OPTIONAL MATCH (f)-[:CLAIMS]->(c:SkillClaim)-[:FOR_SKILL]->(s:Skill)
RETURN f.display_name, collect({skill: s.name, level: c.level, since: c.since}) AS skills;

// name: add_skill
MATCH (f:Freelancer {id: $id}), (s:Skill {name: $skill})
MERGE (f)-[:CLAIMS]->(c:SkillClaim)-[:FOR_SKILL]->(s)
SET c.level = $level, c.since = $since;

// name: contract_page
MATCH (cl:Client)-[:SIGNED]->(k:Contract {id: $id})-[:WITH]->(f:Freelancer)
OPTIONAL MATCH (k)-[:HAS_MILESTONE]->(m:Milestone)
OPTIONAL MATCH (i:Invoice)-[:BILLS]->(k)
OPTIONAL MATCH (d:Dispute)-[:ABOUT]->(k)
RETURN cl.name, f.display_name, k.rate, k.start, k.end,
       collect(DISTINCT m {.title, .due, .done}) AS milestones,
       collect(DISTINCT i {.number, .amount, .paid}) AS invoices,
       collect(DISTINCT d {.opened, .status}) AS disputes;

// name: open_disputes
MATCH (d:Dispute {status: 'open'})-[:ABOUT]->(k:Contract)-[:WITH]->(f:Freelancer)
RETURN d.opened, k.id, f.display_name
ORDER BY d.opened;
