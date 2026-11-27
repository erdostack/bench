-- db: data/scratch.db
WITH v(fn, ln, t) AS (VALUES ('Ciara', 'Hesketh', 'Sea Swimmers'), ('Ciara', 'Hesketh', 'Quiz Night Teams'), ('Orrin', 'Mallory', 'Shanty Singers'), ('Signe', 'Duggan', 'Book Club'), ('Bartek', 'Lumsden', 'Harbour Rowing Club'), ('Kirsi', 'Oddie', 'Beach Clean Volunteers'), ('Hollis', 'Penhaligon', 'Chess at the Anchor'))
DELETE FROM has_member WHERE person_id IN (
  SELECT p.id FROM v JOIN person p ON p.first_name = v.fn AND p.last_name = v.ln);
