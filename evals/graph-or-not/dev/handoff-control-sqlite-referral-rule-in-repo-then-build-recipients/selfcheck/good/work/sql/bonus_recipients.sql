-- Bonus recipients for a new member (docs/rules/referral-bonus.md): referrer = level 1, their referrer = level 2.
SELECT r1.id AS member_id, 1 AS level
FROM member m JOIN member r1 ON r1.id = m.referred_by
WHERE m.id = :member_id
UNION ALL
SELECT r2.id, 2
FROM member m JOIN member r1 ON r1.id = m.referred_by JOIN member r2 ON r2.id = r1.referred_by
WHERE m.id = :member_id;
