-- Every mailbox a message to list :list_id reaches, through nested lists.
-- `path` holds the lists already entered on this branch; a list already on it is not entered again.
WITH RECURSIVE walk (list_id, path) AS (
    SELECT :list_id, '/' || :list_id || '/'
  UNION ALL
    SELECT m.sublist_id, w.path || m.sublist_id || '/'
    FROM walk w
    JOIN member m ON m.list_id = w.list_id
    WHERE m.sublist_id IS NOT NULL
      AND instr(w.path, '/' || m.sublist_id || '/') = 0
)
SELECT DISTINCT m.address
FROM walk w
JOIN member m ON m.list_id = w.list_id
WHERE m.address IS NOT NULL;
