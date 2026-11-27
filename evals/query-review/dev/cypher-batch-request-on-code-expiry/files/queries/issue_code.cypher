MATCH (a:Account {accountId: $accountId})
CREATE (a)-[:HAS_CODE]->(:OneTimeCode {codeHash: $codeHash, expiresAt: datetime() + duration('PT10M')});
