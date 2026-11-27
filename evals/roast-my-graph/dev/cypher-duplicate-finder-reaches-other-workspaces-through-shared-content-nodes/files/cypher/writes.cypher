// name: add_file
MATCH (w:Workspace {id: $ws})<-[:MEMBER_OF]-(u:User {id: $user_id})
MERGE (b:Blob {sha256: $sha256})
  ON CREATE SET b.size_bytes = $size_bytes
CREATE (f:File {id: $file_id, ws: w.id, name: $name, folder: $folder, uploaded_at: datetime()})
CREATE (f)-[:IN]->(w)
CREATE (f)-[:HAS_CONTENT]->(b)
CREATE (u)-[:UPLOADED]->(f);

// name: share_file
MATCH (f:File {id: $file_id})-[:IN]->(w:Workspace {id: $ws})
MATCH (u:User {id: $with_user})-[:MEMBER_OF]->(w)
MERGE (f)-[:SHARED_WITH]->(u);

// name: remove_file
MATCH (f:File {id: $file_id})-[:IN]->(:Workspace {id: $ws})
DETACH DELETE f;
