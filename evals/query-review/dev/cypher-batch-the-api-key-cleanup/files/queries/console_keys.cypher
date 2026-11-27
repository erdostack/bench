MATCH (:Tenant {tenantId: $tenantId})-[:OWNS]->(k:ApiKey)
RETURN k.keyId AS keyId, k.state AS state, k.expiresAt AS expiresAt
ORDER BY k.createdAt DESC;
