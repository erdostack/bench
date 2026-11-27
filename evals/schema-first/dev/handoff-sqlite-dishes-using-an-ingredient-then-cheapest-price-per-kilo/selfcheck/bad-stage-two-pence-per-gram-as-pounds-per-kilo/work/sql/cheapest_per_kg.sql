SELECT i.ingr_nm AS ingredient, MIN(q.pack_p * 1.0 / q.pack_g) AS pounds_per_kg
FROM quote q JOIN ingr i ON i.ingr_id = q.ingr_id
GROUP BY i.ingr_id, i.ingr_nm
ORDER BY i.ingr_nm;
