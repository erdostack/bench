CREATE INDEX api_key_tenant IF NOT EXISTS FOR (k:ApiKey) ON (k.tenantId);
