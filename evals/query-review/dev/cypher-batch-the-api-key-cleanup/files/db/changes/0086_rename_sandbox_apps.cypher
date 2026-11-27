MATCH (a:App) WHERE a.kind = 'sandbox' AND a.name IS NULL
SET a.name = 'Sandbox ' + a.appId;
