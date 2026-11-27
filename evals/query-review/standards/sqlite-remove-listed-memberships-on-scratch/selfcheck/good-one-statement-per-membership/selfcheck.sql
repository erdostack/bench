-- db: data/scratch.db
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Sea Swimmers') AND person_id = (SELECT id FROM person WHERE first_name = 'Ciara' AND last_name = 'Hesketh');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Quiz Night Teams') AND person_id = (SELECT id FROM person WHERE first_name = 'Ciara' AND last_name = 'Hesketh');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Shanty Singers') AND person_id = (SELECT id FROM person WHERE first_name = 'Orrin' AND last_name = 'Mallory');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Book Club') AND person_id = (SELECT id FROM person WHERE first_name = 'Signe' AND last_name = 'Duggan');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Harbour Rowing Club') AND person_id = (SELECT id FROM person WHERE first_name = 'Bartek' AND last_name = 'Lumsden');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Beach Clean Volunteers') AND person_id = (SELECT id FROM person WHERE first_name = 'Kirsi' AND last_name = 'Oddie');
DELETE FROM has_member WHERE forum_id = (SELECT id FROM forum WHERE title = 'Chess at the Anchor') AND person_id = (SELECT id FROM person WHERE first_name = 'Hollis' AND last_name = 'Penhaligon');
