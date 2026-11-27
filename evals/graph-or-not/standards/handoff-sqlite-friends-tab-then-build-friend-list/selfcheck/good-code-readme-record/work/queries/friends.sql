-- account_state 2 = closed (see the table); legal: never list closed friends (README, Decisions)
SELECT k.person2_id AS friend_id, k.creation_date AS since, p.first_name, p.last_name
FROM person_knows_person k JOIN person p ON p.id = k.person2_id
WHERE k.person1_id = :person_id AND p.state <> 2
UNION ALL
SELECT k.person1_id, k.creation_date, p.first_name, p.last_name
FROM person_knows_person k JOIN person p ON p.id = k.person1_id
WHERE k.person2_id = :person_id AND p.state <> 2
ORDER BY since DESC;
