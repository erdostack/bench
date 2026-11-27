// name: load_students
UNWIND $rows AS row
MERGE (s:Student {student_id: row.student_id})
SET s.name = row.name, s.entry_year = row.entry_year;

// name: load_courses
UNWIND $rows AS row
MERGE (c:Course {code: row.code})
SET c.title = row.title,
    c.credits = row.credits,
    c.prerequisite_codes = row.prerequisite_codes   // as exported, e.g. "MATH101,MATH102"
MERGE (d:Department {code: row.department})
MERGE (c)-[:OFFERED_BY]->(d);

// name: load_enrollments
UNWIND $rows AS row
MERGE (e:Enrollment {enrollment_id: row.enrollment_id})
SET e.student_id = row.student_id,
    e.course_code = row.course_code,
    e.term = row.term,
    e.grade = row.grade
WITH e, row
MATCH (s:Student {student_id: row.student_id})
MATCH (c:Course {code: row.course_code})
MERGE (s)-[:HAS_ENROLLMENT]->(e)
MERGE (e)-[:ENROLLMENT_FOR]->(c);
