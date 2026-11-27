WITH v(fn, ln, t) AS (VALUES ('Ciara', 'Hesketh', 'Sea Swimmers'), ('Ciara', 'Hesketh', 'Quiz Night Teams'), ('Orrin', 'Mallory', 'Shanty Singers'), ('Signe', 'Duggan', 'Book Club'), ('Bartek', 'Lumsden', 'Harbour Rowing Club'), ('Kirsi', 'Oddie', 'Beach Clean Volunteers'), ('Hollis', 'Penhaligon', 'Chess at the Anchor'))
DELETE FROM has_member WHERE (forum_id, person_id) IN (
  SELECT f.id, p.id FROM v JOIN person p ON p.first_name = v.fn AND p.last_name = v.ln JOIN forum f ON f.title = v.t);
