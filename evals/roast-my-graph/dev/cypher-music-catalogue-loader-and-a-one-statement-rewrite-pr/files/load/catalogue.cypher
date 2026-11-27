// name: upsert_artists
UNWIND $rows AS row
MERGE (a:Artist {mbid: row.artist_mbid})
SET a.name = row.artist_name, a.sort_name = row.artist_sort_name;

// name: upsert_releases
UNWIND $rows AS row
MERGE (r:Release {mbid: row.release_mbid})
SET r.title = row.title, r.year = row.year;

// name: link_artists
UNWIND $rows AS row
MATCH (a:Artist {mbid: row.artist_mbid})
MATCH (r:Release {mbid: row.release_mbid})
MERGE (a)-[c:CREDITED_ON]->(r)
SET c.position = row.position, c.join_phrase = row.join_phrase;

// name: link_labels
UNWIND $rows AS row
MATCH (r:Release {mbid: row.release_mbid})
MERGE (l:Label {mbid: row.label_mbid})
  ON CREATE SET l.name = row.label_name
MERGE (r)-[:ON_LABEL]->(l);
