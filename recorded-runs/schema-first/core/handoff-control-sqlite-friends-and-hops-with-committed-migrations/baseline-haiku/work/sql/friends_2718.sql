-- Friends of person 2718, with the date each friendship was accepted.
-- Friendships are stored once, with the smaller id in person1Id, so check both columns.
SELECT p.id AS friend_id, p.firstName, p.lastName, k.creationDate AS friends_since
FROM knows k
JOIN person p ON p.id = CASE WHEN k.person1Id = 2718 THEN k.person2Id ELSE k.person1Id END
WHERE 2718 IN (k.person1Id, k.person2Id)
ORDER BY k.creationDate, p.id;
