CREATE INDEX copy_last_loan IF NOT EXISTS FOR (c:Copy) ON (c.lastLoanAt);
