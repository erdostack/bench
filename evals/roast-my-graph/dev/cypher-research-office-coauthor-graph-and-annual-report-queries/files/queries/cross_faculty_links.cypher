// annual report: collaborations between $faculty and each other faculty
MATCH (a:Researcher)-[c:COAUTHORED]-(b:Researcher)
WHERE a.faculty = $faculty AND b.faculty <> $faculty
RETURN b.faculty AS partner_faculty, count(c) AS collaborations, sum(c.papers) AS joint_papers
ORDER BY collaborations DESC;
