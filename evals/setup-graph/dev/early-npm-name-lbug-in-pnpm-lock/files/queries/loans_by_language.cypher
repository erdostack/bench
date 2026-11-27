// How many English words in the sample were borrowed directly from each language.
MATCH (w:Word {language: 'en'})-[d:DERIVES_FROM]->(source:Word)
WHERE d.kind = 'borrowed'
RETURN source.language AS language, count(w) AS loans
ORDER BY loans DESC, language
