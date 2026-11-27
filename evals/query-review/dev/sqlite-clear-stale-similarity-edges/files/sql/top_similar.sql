-- The ten most similar listings to :listing_id.
-- Columns: id, title, score
SELECT l.id, l.title, e.score
FROM edges e JOIN listings l ON l.id = e.dst
WHERE e.src = :listing_id AND e.kind = 'similar_to'
ORDER BY e.score DESC, l.id
LIMIT 10;
