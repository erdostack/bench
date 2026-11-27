-- Friends tab for :person_id, newest friendship first. Legal (closure policy, docs/graph/DECISION.md): a friend
-- whose account is closed is never listed; suspended and pending friends still show. A closed member has no tab.
SELECT CASE WHEN k.person1_id = :person_id THEN k.person2_id ELSE k.person1_id END AS friend_id,
       k.creation_date AS since
FROM person_knows_person AS k
JOIN person AS friend
  ON friend.id = CASE WHEN k.person1_id = :person_id THEN k.person2_id ELSE k.person1_id END
WHERE :person_id IN (k.person1_id, k.person2_id)
  AND friend.state NOT IN (SELECT code FROM account_state WHERE label = 'closed')
  AND NOT EXISTS (SELECT 1 FROM person AS me JOIN account_state AS s ON s.code = me.state
                  WHERE me.id = :person_id AND s.label = 'closed')
ORDER BY since DESC;
