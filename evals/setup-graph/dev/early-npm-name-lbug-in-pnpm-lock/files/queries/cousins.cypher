// English words that share an ancestor with $word, and the ancestor they share.
MATCH (w:Word {form: $word, language: 'en'})-[:DERIVES_FROM*1..8]->(root:Word)<-[:DERIVES_FROM*1..8]-(other:Word {language: 'en'})
WHERE other.id <> w.id
RETURN DISTINCT other.form AS word, root.form AS shared_root, root.language AS root_language
ORDER BY word
