Last night's run was the first version: for images 1-1100 it wrote one image_component row per SBOM line
(a component listed in three layers got three rows) and counted lines, so those are wrong, and the current
job would add the distinct rows on top of them and add to the counts again. I changed the job so each batch
deletes the batch's images' edges, inserts the distinct set and sets component_count from what it inserted,
in one transaction. Re-running or a kill at any point is harmless, and it repairs 1-1100 on the way.
Batches of 10 images keep every transaction under 2,000 changed rows (largest about 1,300 on a copy).
Check after: `SELECT count(*) FROM (SELECT image_id, component_id FROM image_component GROUP BY 1, 2 HAVING count(*) > 1)` is 0.
