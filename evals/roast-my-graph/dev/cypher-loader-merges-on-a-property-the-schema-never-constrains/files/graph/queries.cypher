// name: artwork_page
MATCH (a:Artwork {accession_no: $accession_no})
OPTIONAL MATCH (a)-[r:MADE_BY]->(m:Maker)
RETURN a.title AS title, a.dated AS dated, a.department AS department,
       collect({maker: m.name, role: r.role}) AS makers;

// name: maker_page
MATCH (m:Maker {id: $maker_id})<-[:MADE_BY]-(a:Artwork)
RETURN a.accession_no AS accession_no, a.title AS title, a.dated AS dated
ORDER BY a.dated
LIMIT 200;

// name: maker_search
MATCH (m:Maker)
WHERE m.name STARTS WITH $prefix
RETURN m.id AS id, m.name AS name
ORDER BY m.name
LIMIT 20;

// name: on_loan_at
MATCH (v:Venue {code: $venue_code})<-[l:ON_LOAN_TO]-(a:Artwork)
WHERE l.ends >= date()
RETURN a.accession_no AS accession_no, a.title AS title, l.ends AS ends
ORDER BY l.ends;

// name: department_browse
MATCH (a:Artwork)
WHERE a.department = $department
RETURN a.accession_no AS accession_no, a.title AS title
ORDER BY a.accession_no
SKIP $offset LIMIT 48;
