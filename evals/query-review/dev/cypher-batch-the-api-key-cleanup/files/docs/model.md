# Model

- `(:Tenant {tenantId})-[:OWNS]->(:ApiKey {keyId, tenantId, state, createdAt, expiresAt})`
- `(:ApiKey)-[:FOR_APP]->(:App {appId})`
- `(:ApiKey)-[:USED {day, calls}]->(:UsageDay)`: daily usage, kept 90 days

`state` is `active`, `expired` or `revoked`. Counts (2026-11-15): 41 million keys for 380,000
tenants; 3.1 million revoked and 9.6 million expired across the platform. `tenantId` is copied
onto the key so the gateway can check it without a hop; index `api_key_tenant` on it.
