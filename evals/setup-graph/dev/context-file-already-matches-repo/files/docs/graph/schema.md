# Schema snapshot

Taken from `sql/schema.sql` (the file the database container is initialised with).

## Tables

| Table | Column | Type | Notes |
|---|---|---|---|
| course | code | text | primary key |
| course | title | text | not null |
| course | credits | smallint | not null, > 0 |
| prerequisite | course | text | references course(code) |
| prerequisite | needs | text | references course(code) |

## Edges

`prerequisite` is the edge table. Direction: `course` needs `needs`, i.e. an edge points from a course to the
course that must be passed first. Primary key (course, needs); a course cannot require itself.

## Indexes

- `prerequisite_needs` on prerequisite(needs), for "what does this course unlock"
