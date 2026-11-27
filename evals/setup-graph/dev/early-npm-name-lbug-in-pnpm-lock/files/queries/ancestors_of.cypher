// The chain of earlier forms behind $word (English), nearest first.
MATCH path = (w:Word {form: $word, language: 'en'})-[:DERIVES_FROM*1..8]->(older:Word)
RETURN older.form AS form, older.language AS language, older.gloss AS gloss, length(path) AS steps
ORDER BY steps
