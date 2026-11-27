-- The member's friends for the Friends tab: one row per friend whose account is active, with the friendship's
-- creation_date as stored, newest first. A friendship is stored once with person1_id < person2_id, so the friend
-- is whichever side is not :person_id.
WITH friendship AS (
  SELECT person2_id AS friend_id, creation_date
  FROM person_knows_person
  WHERE person1_id = :person_id
  UNION ALL
  SELECT person1_id AS friend_id, creation_date
  FROM person_knows_person
  WHERE person2_id = :person_id
)
SELECT f.friend_id AS friend_id,
       f.creation_date AS since
FROM friendship f
JOIN person p ON p.id = f.friend_id
JOIN account_state s ON s.code = p.state
WHERE s.label = 'active'
ORDER BY f.creation_date DESC, f.friend_id DESC;
