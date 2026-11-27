SELECT k.person2_id AS friend_id, k.creation_date AS since
FROM person_knows_person k
JOIN person p ON p.id = k.person2_id
JOIN account_state s ON s.code = p.state
WHERE k.person1_id = :person_id AND s.label <> 'closed'
ORDER BY since DESC;
