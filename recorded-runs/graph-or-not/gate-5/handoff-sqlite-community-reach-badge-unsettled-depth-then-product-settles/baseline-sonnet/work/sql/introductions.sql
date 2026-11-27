-- Badge: 1 if :viewer_id and :member_id follow each other in either direction, 2 if they share a
-- connection (someone either one follows or is followed by), otherwise no row.
-- Two bounded lookups on the primary key and on follow_followed; no recursion.
SELECT 1 AS steps
WHERE EXISTS (SELECT 1 FROM follow WHERE follower_id = :viewer_id AND followed_id = :member_id)
   OR EXISTS (SELECT 1 FROM follow WHERE follower_id = :member_id AND followed_id = :viewer_id)
UNION ALL
SELECT 2
WHERE EXISTS (
    SELECT 1
    FROM (SELECT followed_id AS x FROM follow WHERE follower_id = :viewer_id
          UNION SELECT follower_id FROM follow WHERE followed_id = :viewer_id) v
    JOIN (SELECT followed_id AS x FROM follow WHERE follower_id = :member_id
          UNION SELECT follower_id FROM follow WHERE followed_id = :member_id) m ON m.x = v.x
)
ORDER BY 1
LIMIT 1;
