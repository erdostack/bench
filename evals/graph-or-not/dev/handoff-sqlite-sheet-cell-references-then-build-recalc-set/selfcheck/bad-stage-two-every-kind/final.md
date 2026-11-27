Added sql/recalc_set.sql. It follows every row in `ref` from the edited cell (formulas, charts, validation
and conditional formats all read values, so all of them need refreshing), with UNION so circular references
end.
