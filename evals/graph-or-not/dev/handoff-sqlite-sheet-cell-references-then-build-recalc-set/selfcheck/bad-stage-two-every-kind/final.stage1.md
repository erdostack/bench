Decision: recursive-sql

The workbook file is already open when the edit arrives, and the question is "what is downstream of this one cell",
so a recursive query on `ref` (it has `ref_by_dst`) does it where the data is.

- Two things the query has to respect: only formula references count (charts, validation and conditional formats
  redraw on their own), and 3% of workbooks have circular references, so the walk must use UNION over (sheet,
  addr) and no depth column, or it goes round a cycle forever.
- Even the biggest workbook is 210k references; the part downstream of one cell is a fraction of that, well inside
  100 ms on an index.
- A graph database means copying every workbook into another store and keeping 900 edits a second in step.
- Loading the references into a graph library on each edit reads the whole file every time, since nothing stays in
  memory between edits.
