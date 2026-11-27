sql/recalc_set.sql is in. It starts from the edited cell and follows formula references only (the record in
docs/graph/DECISION.md says charts, validation and conditional formats don't drive recalc), with UNION so the
circular references terminate. I left the edited cell in the result so the caller can recalc everything in one
pass. Tested on a small synthetic workbook I built in memory with 14 cells and a 2-cell cycle: 9 rows, no hang.
