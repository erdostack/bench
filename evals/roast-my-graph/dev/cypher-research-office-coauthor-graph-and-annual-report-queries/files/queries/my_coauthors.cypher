MATCH (me:Researcher {orcid: $orcid})-[c:COAUTHORED]-(other:Researcher)
RETURN other.name, other.faculty, c.papers
ORDER BY c.papers DESC, other.name;
