WITH RECURSIVE up (member_id, level) AS (
    SELECT referred_by, 1 FROM member WHERE id = :member_id AND referred_by IS NOT NULL
    UNION ALL
    SELECT m.referred_by, up.level + 1 FROM up JOIN member m ON m.id = up.member_id
    WHERE m.referred_by IS NOT NULL AND up.level < 100
)
SELECT member_id, level FROM up;
