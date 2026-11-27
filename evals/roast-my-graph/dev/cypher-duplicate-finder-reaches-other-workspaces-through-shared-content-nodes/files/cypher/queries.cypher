// name: list_folder
MATCH (f:File)
WHERE f.ws = $ws AND f.folder = $folder
RETURN f.id AS id, f.name AS name, f.uploaded_at AS uploaded_at
ORDER BY f.name
LIMIT 500;

// name: file_details
MATCH (f:File {id: $file_id})-[:IN]->(:Workspace {id: $ws})
MATCH (f)-[:HAS_CONTENT]->(b:Blob)
OPTIONAL MATCH (up:User)-[:UPLOADED]->(f)
RETURN f.name AS name, f.folder AS folder, b.sha256 AS sha256, b.size_bytes AS size_bytes, up.id AS uploaded_by;

// name: duplicates_of
MATCH (f:File {id: $file_id})-[:IN]->(:Workspace {id: $ws})
MATCH (f)-[:HAS_CONTENT]->(b:Blob)<-[:HAS_CONTENT]-(other:File)
WHERE other <> f
RETURN other.id AS id, other.name AS name, other.folder AS folder
ORDER BY other.folder, other.name
LIMIT 200;

// name: shared_with_me
MATCH (u:User {id: $user_id})<-[:SHARED_WITH]-(f:File)-[:IN]->(:Workspace {id: $ws})
RETURN f.id AS id, f.name AS name, f.folder AS folder
ORDER BY f.uploaded_at DESC
LIMIT 200;

// name: my_uploads
MATCH (u:User {id: $user_id})-[:UPLOADED]->(f:File)-[:IN]->(:Workspace {id: $ws})
RETURN f.id AS id, f.name AS name, f.folder AS folder
ORDER BY f.uploaded_at DESC
LIMIT 200;
