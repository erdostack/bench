-- The member's friends for the Friends tab, newest friendship first. Closed accounts (state 2) are never listed;
-- suspended and pending-verification members are.
SELECT f.friend_id AS friend_id, f.since AS since
FROM (
    SELECT person2_id AS friend_id, creation_date AS since
    FROM person_knows_person
    WHERE person1_id = :person_id
    UNION ALL
    SELECT person1_id AS friend_id, creation_date AS since
    FROM person_knows_person
    WHERE person2_id = :person_id
) AS f
JOIN person AS p ON p.id = f.friend_id
WHERE p.state <> 2
ORDER BY f.since DESC, f.friend_id;
