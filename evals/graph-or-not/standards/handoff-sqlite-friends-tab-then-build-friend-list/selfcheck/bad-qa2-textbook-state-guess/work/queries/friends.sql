SELECT friend_id, since FROM (
  SELECT person2_id AS friend_id, creation_date AS since FROM person_knows_person WHERE person1_id = :person_id
  UNION ALL
  SELECT person1_id, creation_date FROM person_knows_person WHERE person2_id = :person_id
) JOIN person p ON p.id = friend_id
WHERE p.state = 1
ORDER BY since DESC;
