CREATE INDEX transfer_settled IF NOT EXISTS FOR (t:Transfer) ON (t.settledAt);
