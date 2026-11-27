sql/equivalents.sql done. Per ADR 0005 it counts every pair that is not withdrawn (approved and provisional), reads
each pair both ways, and stops the recursion at 41 links: the largest group on record is 41 courses, so no shortest
chain can be longer, and the bound is what keeps the walk from going round the loops forever. MIN(links) per course,
the course itself left out.
