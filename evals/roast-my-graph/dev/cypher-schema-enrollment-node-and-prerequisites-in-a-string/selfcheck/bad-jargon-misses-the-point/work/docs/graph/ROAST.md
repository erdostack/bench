# Roast: coursegraph

Tables in a trench coat! This schema has every anti-pattern in the catalogue, so here is the catalogue.

## Findings

### 1. Enrollment (high)

**Problem.** Textbook join-table-as-a-node smell: the Enrollment label has no existence constraint on term or grade, and its uniqueness constraint overlaps the two range indexes.

**Fix.** Add property existence constraints for term and grade and replace the two indexes with one composite index on (student_id, course_code) so the join node is properly normalised.

### 2. Course.prerequisite_codes (medium)

**Problem.** Everything-as-a-property anti-pattern: prerequisite_codes has no declared type, so the split() in can_take may receive a non-string.

**Fix.** Add a property type constraint so prerequisite_codes is always a STRING, and add a text index on it so the planner can search it faster.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
