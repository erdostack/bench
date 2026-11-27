// expire issued referrals May to July.
MATCH (r:Referral {status: 'issued'}) WHERE r.issuedAt >= '2026-05-01' AND r.issuedAt < '2026-08-01'
CALL (r) { SET r.status = 'expired' } IN TRANSACTIONS OF 5000 ROWS;
