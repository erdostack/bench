Added sql/equivalents.sql. The recursive part follows course_equivalence from either column and keeps approved and
provisional pairs; UNION drops duplicate rows, and the outer query keeps the fewest links per course.
