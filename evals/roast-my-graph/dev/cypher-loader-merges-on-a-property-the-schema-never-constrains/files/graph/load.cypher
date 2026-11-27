// name: load_makers
UNWIND $rows AS row
MERGE (m:Maker {id: row.maker_id})
SET m.name = row.name, m.born = row.born, m.died = row.died;

// name: load_artworks
UNWIND $rows AS row
MERGE (a:Artwork {accession_no: row.accession_no})
SET a.title = row.title,
    a.department = row.department,
    a.dated = row.dated,
    a.catalogue_id = row.catalogue_id;

// name: load_attributions
UNWIND $rows AS row
MATCH (a:Artwork {accession_no: row.accession_no})
MATCH (m:Maker {id: row.maker_id})
MERGE (a)-[r:MADE_BY]->(m)
SET r.role = row.role;

// name: load_loans
UNWIND $rows AS row
MATCH (a:Artwork {accession_no: row.accession_no})
MERGE (v:Venue {code: row.venue_code})
SET v.name = row.venue_name
MERGE (a)-[l:ON_LOAN_TO]->(v)
SET l.starts = date(row.starts), l.ends = date(row.ends);
