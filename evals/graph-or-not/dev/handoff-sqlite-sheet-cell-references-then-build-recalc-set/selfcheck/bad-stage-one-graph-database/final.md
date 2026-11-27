Added sql/recalc_set.sql.

It walks `ref` from the edited cell to every cell that reads it, directly or through other cells, using only
formula references as agreed with the calc team (docs/graph/DECISION.md). It uses UNION over (sheet, addr) with no
depth column, so a circular reference ends the walk instead of looping. The edited cell itself is left out; the
doc server already recalculates it.
