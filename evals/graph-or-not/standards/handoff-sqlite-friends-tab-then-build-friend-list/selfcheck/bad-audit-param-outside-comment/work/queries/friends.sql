-- Friends tab: the friends of :person_id and the date each friendship began; newest first.
-- A friend's account that's closed is left out (see docs/graph/DECISION.md); suspended ones still show.
SELECT f.friend_id, f.since
FROM (
    SELECT person2_id AS friend_id, creation_date AS since FROM person_knows_person WHERE person1_id = :member_id
    UNION ALL
    SELECT person1_id, creation_date FROM person_knows_person WHERE person2_id = :member_id
) AS f
JOIN person p ON p.id = f.friend_id
JOIN account_state s ON s.code = p.state
WHERE s.label <> 'closed'
ORDER BY f.since DESC, f.friend_id;
