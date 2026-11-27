// name: institute_collaboration
MATCH (a:Researcher)-[c:COAUTHORED]-(b:Researcher)
WHERE a.institute = $institute AND b.institute = $institute
RETURN count(c) AS collaborating_pairs, avg(c.papers) AS papers_per_pair;

// name: institute_headcount
MATCH (r:Researcher {institute: $institute})
RETURN count(r) AS researchers;
