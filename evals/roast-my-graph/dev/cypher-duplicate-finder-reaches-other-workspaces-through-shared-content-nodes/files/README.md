# vaultshelf

Document storage for small professional firms (mostly law and accounting practices). Each customer gets a
workspace. File metadata and sharing live in Neo4j 5; the bytes are in object storage.

    docs/model.md            the model
    cypher/schema.cypher     constraints and indexes
    cypher/writes.cypher     statements the upload service runs
    cypher/queries.cypher    statements the web app runs; each has a `// name:` line

2,300 workspaces, 41,000 users, 96 million files.

## Workspace isolation

A user belongs to one workspace and must never learn anything about another one, not even that a file
exists there. The web app takes the workspace id from the session token and passes it to every query as
`$ws`; `$user_id` comes from the same token. Everything else in a request (`$file_id`, `$folder`) is typed
or clicked by the user and is not trusted.
