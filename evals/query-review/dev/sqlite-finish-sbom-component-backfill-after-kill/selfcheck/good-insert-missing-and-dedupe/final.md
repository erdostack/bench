Made each batch idempotent: remove the first version's duplicate rows, insert the missing distinct ones, set counts from the rows. Kill-safe.
