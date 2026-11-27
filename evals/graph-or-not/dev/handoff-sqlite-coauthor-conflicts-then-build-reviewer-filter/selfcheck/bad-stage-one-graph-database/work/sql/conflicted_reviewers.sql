-- Researchers with a conflict of interest on a submission (editor-in-chief's rule):
-- co-authored a paper with any of the submission's authors in the last 24 months.
-- Direct co-authors only; institutions do not count. The submission's own authors are left out.
SELECT DISTINCT co.researcher_id
FROM submission_author sa
JOIN authorship mine ON mine.researcher_id = sa.researcher_id
JOIN paper p         ON p.id = mine.paper_id
JOIN authorship co   ON co.paper_id = p.id
WHERE sa.submission_id = :submission_id
  AND p.published_on >= date(:today, '-24 months')
  AND co.researcher_id NOT IN (SELECT researcher_id FROM submission_author WHERE submission_id = :submission_id);
