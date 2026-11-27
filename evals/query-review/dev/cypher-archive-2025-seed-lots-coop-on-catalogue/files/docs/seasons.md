# End of season

When a season closes, its lots are archived: `SET s:Archived REMOVE s:Active`, so the ordering site stops
listing them while the reports still find them.

A lot that still has stock (`qty_kg > 0`) is not archived. It is carried over: it stays `:Active` and the
seed team re-tags it with the next season's germination test in spring.
