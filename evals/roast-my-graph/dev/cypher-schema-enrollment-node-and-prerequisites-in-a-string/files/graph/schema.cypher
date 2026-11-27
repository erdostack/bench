CREATE CONSTRAINT student_id IF NOT EXISTS FOR (s:Student) REQUIRE s.student_id IS UNIQUE;
CREATE CONSTRAINT course_code IF NOT EXISTS FOR (c:Course) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT department_code IF NOT EXISTS FOR (d:Department) REQUIRE d.code IS UNIQUE;
CREATE CONSTRAINT enrollment_id IF NOT EXISTS FOR (e:Enrollment) REQUIRE e.enrollment_id IS UNIQUE;

CREATE INDEX enrollment_student IF NOT EXISTS FOR (e:Enrollment) ON (e.student_id);
CREATE INDEX enrollment_course IF NOT EXISTS FOR (e:Enrollment) ON (e.course_code);
