// name: transcript
MATCH (s:Student {student_id: $student_id})-[:HAS_ENROLLMENT]->(e:Enrollment)-[:ENROLLMENT_FOR]->(c:Course)
RETURN e.term AS term, c.code AS code, c.title AS title, e.grade AS grade
ORDER BY term, code;

// name: classmates
MATCH (me:Student {student_id: $student_id})-[:HAS_ENROLLMENT]->(mine:Enrollment)-[:ENROLLMENT_FOR]->(c:Course)
      <-[:ENROLLMENT_FOR]-(theirs:Enrollment)<-[:HAS_ENROLLMENT]-(other:Student)
WHERE mine.term = theirs.term AND other <> me
RETURN other.name AS name, count(DISTINCT c) AS shared_courses
ORDER BY shared_courses DESC
LIMIT 25;

// name: department_load
MATCH (d:Department {code: $department})<-[:OFFERED_BY]-(c:Course)<-[:ENROLLMENT_FOR]-(e:Enrollment)
WHERE e.term = $term
RETURN c.code AS code, count(e) AS seats_taken
ORDER BY seats_taken DESC;

// name: prerequisite_chain
// Everything needed before a course, all the way down. The planner calls this once per
// level and stitches the levels together itself.
MATCH (c:Course {code: $course_code})
RETURN c.code AS code, c.prerequisite_codes AS needs;

// name: can_take
MATCH (c:Course {code: $course_code})
MATCH (s:Student {student_id: $student_id})
WITH s, [code IN split(coalesce(c.prerequisite_codes, ''), ',') WHERE code <> ''] AS needed
OPTIONAL MATCH (s)-[:HAS_ENROLLMENT]->(e:Enrollment)
WHERE e.course_code IN needed AND e.grade IN ['A', 'B', 'C', 'D']
RETURN size(needed) = count(DISTINCT e.course_code) AS eligible;
