// name: package_page
MATCH (p:Package {name: $name})
OPTIONAL MATCH (p)-[:LICENSED_UNDER]->(l:License)
OPTIONAL MATCH (m:Maintainer)-[:MAINTAINS]->(p)
RETURN p.name AS name, p.description AS description, p.latest_version AS version,
       l.spdx AS license, collect(m.handle) AS maintainers;

// name: related_packages
MATCH (p:Package {name: $name})-[:LICENSED_UNDER]->(l:License)<-[:LICENSED_UNDER]-(other:Package)
WHERE other <> p AND other.category = p.category
RETURN other.name AS name, other.description AS description
ORDER BY other.weekly_downloads DESC
LIMIT 8;
