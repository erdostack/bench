// name: profile
MATCH (l:Learner {id: $learner})
RETURN l.display_name AS name,
       [(l)-[:SPEAKS]->(g:Language) | g.code] AS speaks,
       [(l)-[x:LEARNING]->(g:Language) | {code: g.code, level: x.level}] AS learning;

// name: learner_home
MATCH (l:Learner {id: $learner})-[e:ENROLLED_IN]->(c:Course)-[:TEACHES]->(g:Language)
RETURN c.id AS course, c.title AS title, g.code AS language, e.since AS since
ORDER BY e.since DESC;

// name: next_lessons
MATCH (l:Learner {id: $learner})-[e:ENROLLED_IN]->(c:Course {id: $course})-[:HAS]->(s:Lesson)
WHERE s.position >= e.next_position
RETURN s.id AS lesson, s.title AS title, s.position AS position
ORDER BY s.position
LIMIT 5;

// name: course_list
MATCH (c:Course)-[:TEACHES]->(g:Language)
WHERE c.published
RETURN c.id AS id, c.title AS title, g.code AS language, c.cefr_level AS level
ORDER BY g.code, c.cefr_level, c.title;

// name: set_learning
MATCH (l:Learner {id: $learner})
MATCH (g:Language {code: $language})
MERGE (l)-[x:LEARNING]->(g)
SET x.level = $level;

// name: enrol
MATCH (l:Learner {id: $learner})
MATCH (c:Course {id: $course})
MERGE (l)-[e:ENROLLED_IN]->(c)
  ON CREATE SET e.since = datetime(), e.next_position = 1;

// name: finish_lesson
// every finish is kept (learners redo lessons; the streak calendar shows each one)
MATCH (l:Learner {id: $learner})-[e:ENROLLED_IN]->(c:Course)-[:HAS]->(s:Lesson {id: $lesson})
CREATE (l)-[:FINISHED {at: datetime()}]->(s)
SET e.next_position = CASE WHEN s.position + 1 > e.next_position THEN s.position + 1
                           ELSE e.next_position END;
