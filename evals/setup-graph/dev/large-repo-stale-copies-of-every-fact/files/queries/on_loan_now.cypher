// Objects out on loan on $today, with the borrower and the end date.
MATCH (o:Object)-[:PART_OF]->(l:Loan)-[:TO]->(borrower:Institution)
WHERE l.starts <= date($today) AND (l.ends IS NULL OR l.ends >= date($today))
RETURN o.accession AS accession, o.title AS title, borrower.name AS borrower, toString(l.ends) AS ends
ORDER BY ends, accession
