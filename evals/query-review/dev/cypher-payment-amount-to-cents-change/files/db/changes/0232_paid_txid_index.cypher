CREATE INDEX paid_txid IF NOT EXISTS FOR ()-[p:PAID]-() ON (p.txId);
