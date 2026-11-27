WITH RECURSIVE net(researcher_id, hops) AS (
    SELECT researcher_id, 0 FROM submission_author WHERE submission_id = :submission_id
    UNION
    SELECT co.researcher_id, n.hops + 1
    FROM net n
    JOIN authorship mine ON mine.researcher_id = n.researcher_id
    JOIN paper p ON p.id = mine.paper_id AND p.published_on >= date(:today, '-24 months')
    JOIN authorship co ON co.paper_id = p.id
    WHERE n.hops < 2
)
SELECT DISTINCT researcher_id FROM net
WHERE researcher_id NOT IN (SELECT researcher_id FROM submission_author WHERE submission_id = :submission_id);
