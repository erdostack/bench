WITH authors AS (
    SELECT researcher_id FROM submission_author WHERE submission_id = :submission_id
),
recent AS (
    SELECT id FROM paper WHERE published_on >= date(:today, '-2 years') AND published_on <= :today
)
SELECT a2.researcher_id
FROM authorship a1
JOIN recent r ON r.id = a1.paper_id
JOIN authorship a2 ON a2.paper_id = a1.paper_id
WHERE a1.researcher_id IN (SELECT researcher_id FROM authors)
EXCEPT
SELECT researcher_id FROM authors;
