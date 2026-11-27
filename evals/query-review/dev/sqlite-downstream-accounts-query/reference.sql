WITH RECURSIVE reach(id) AS (
    SELECT dst FROM transfers WHERE src = :src
    UNION
    SELECT t.dst FROM reach r JOIN transfers t ON t.src = r.id
)
SELECT id AS account_id FROM reach WHERE id <> :src;
