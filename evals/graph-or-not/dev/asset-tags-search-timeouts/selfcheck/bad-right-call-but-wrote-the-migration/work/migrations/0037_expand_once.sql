CREATE OR REPLACE FUNCTION expanded_tag_ids(root integer) RETURNS SETOF integer
LANGUAGE sql STABLE AS $$
    WITH RECURSIVE down (id) AS (
        SELECT root
        UNION
        SELECT i.narrower_id FROM tag_implications i JOIN down d ON i.broader_id = d.id
    )
    SELECT id FROM down
$$;
