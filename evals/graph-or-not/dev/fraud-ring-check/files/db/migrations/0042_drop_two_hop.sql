-- 0042: remove account_two_hop.
-- Added in 0038 as a precomputed "accounts within two steps" table so the ring check could start
-- from it. Reached 6.4 billion rows after backfilling 60% of accounts; the incremental refresh fell
-- nine hours behind at normal write volume and the table was never read by the service.
DROP TABLE IF EXISTS account_two_hop;
DROP FUNCTION IF EXISTS refresh_account_two_hop(bigint);
