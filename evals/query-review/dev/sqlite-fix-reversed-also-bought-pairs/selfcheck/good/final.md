Wrote jobs/fix_reversed_also_bought.py. 11,000 rows have a > b; 7,000 of them are pairs that also have a correct
a < b row (bought again during the bad days), so simply swapping the columns would hit the primary key, and
INSERT OR REPLACE would throw away one of the two counts. The job adds each reversed row's orders to the a < b row
(upsert, creating it when there is none) and deletes the reversed row, 500 rows per transaction (1,000 changes).
Returns 11,000 on a copy of var/recs.db; afterwards `SELECT count(*) FROM also_bought WHERE a > b` is 0 and the
total of orders is unchanged.
