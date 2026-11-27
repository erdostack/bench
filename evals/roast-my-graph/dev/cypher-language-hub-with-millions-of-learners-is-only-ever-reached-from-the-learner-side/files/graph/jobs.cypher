// name: language_totals
MATCH (g:Language)
RETURN g.code AS language,
       COUNT { (g)<-[:SPEAKS]-(:Learner) } AS speakers,
       COUNT { (g)<-[:LEARNING]-(:Learner) } AS learners
ORDER BY learners DESC;
