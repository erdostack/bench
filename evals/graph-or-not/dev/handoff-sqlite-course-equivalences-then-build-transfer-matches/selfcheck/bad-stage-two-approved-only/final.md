Added sql/equivalents.sql, a recursive query as the decision says. Only approved pairs count, since provisional ones
have not been reviewed by the department yet and withdrawn ones are void. Pairs are read both ways and the walk
tracks visited courses so it terminates. Returns (course_id, links), fewest links, without the course itself.
