-- Friends tab for :person_id, newest friendship first. Friends whose account is closed are never listed
-- (legal, docs/graph/DECISION.md); the closed code is looked up by label in account_state.
SELECT CASE WHEN k.person1_id = :person_id THEN k.person2_id ELSE k.person1_id END AS friend_id,
       k.creation_date AS since
FROM person_knows_person k
JOIN person f ON f.id = CASE WHEN k.person1_id = :person_id THEN k.person2_id ELSE k.person1_id END
WHERE :person_id IN (k.person1_id, k.person2_id)
  AND f.state NOT IN (SELECT code FROM account_state WHERE label = 'closed')
ORDER BY since DESC;
