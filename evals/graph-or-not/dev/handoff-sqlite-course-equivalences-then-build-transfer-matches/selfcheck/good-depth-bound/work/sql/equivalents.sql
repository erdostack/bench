with recursive
  edges(src, dst) as (
    select course_a, course_b from course_equivalence where status <> 'withdrawn'
    union
    select course_b, course_a from course_equivalence where status <> 'withdrawn'
  ),
  reach(course_id, links) as (
    select :course_id, 0
    union
    select e.dst, r.links + 1 from reach r join edges e on e.src = r.course_id
    where r.links < 41     -- the largest known group is 41 courses, so no shortest chain is longer
  )
select course_id, min(links) from reach where course_id != :course_id group by course_id
