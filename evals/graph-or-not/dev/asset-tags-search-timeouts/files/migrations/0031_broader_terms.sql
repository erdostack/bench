-- The archive desk's thesaurus, imported 2026-03-18 at the curators' request.
--
-- Every thesaurus term is a row in tags. A term can sit under several broader terms ("Bauhaus" is under
-- both "Modernism" and "Design schools"), so this is not a tree. The deepest branch is 11 levels.
-- Searching a term has to return assets tagged with any narrower term, at any depth: an editor who
-- searches "Architecture" expects the Bauhaus pictures.
--
-- The three curators edit it through the thesaurus screen, about a dozen changes a week.

CREATE TABLE tag_implications (
    narrower_id  integer NOT NULL REFERENCES tags (id),
    broader_id   integer NOT NULL REFERENCES tags (id),
    PRIMARY KEY (narrower_id, broader_id),
    CHECK (narrower_id <> broader_id)
);
CREATE INDEX tag_implications_broader_idx ON tag_implications (broader_id);

-- The searched term and everything under it.
CREATE FUNCTION expanded_tag_ids(root integer) RETURNS SETOF integer
LANGUAGE sql STABLE AS $$
    WITH RECURSIVE down (id) AS (
        SELECT root
        UNION ALL
        SELECT i.narrower_id
        FROM tag_implications i
        JOIN down d ON i.broader_id = d.id
    )
    SELECT id FROM down
$$;
