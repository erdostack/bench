-- Friends of person 2129 and the date each friendship started.
-- knows stores an unordered pair once (CHECK person1Id < person2Id), so the friend is the other column.
-- knows.creationDate is the day the friendship was accepted (ISO text YYYY-MM-DD).
SELECT p.id AS friend_id, p.firstName, p.lastName, k.creationDate
FROM knows k
JOIN person p ON p.id = CASE WHEN k.person1Id = 2129 THEN k.person2Id ELSE k.person1Id END
WHERE k.person1Id = 2129 OR k.person2Id = 2129
ORDER BY k.creationDate, p.id;
