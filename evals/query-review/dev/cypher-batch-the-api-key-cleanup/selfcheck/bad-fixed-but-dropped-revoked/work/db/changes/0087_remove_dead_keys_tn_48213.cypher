MATCH (k:ApiKey {tenantId: 'tn_48213'})
WHERE k.state = 'expired'
DETACH DELETE k;
