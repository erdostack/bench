It would not have finished cleanly: batch 6401-6800 committed, then the progress write failed, so job_progress
said 6400 and the retry would insert those ~770 legs again (leg has no unique key). I set job_progress to 6800
in var/parcels.db, so tonight's run resumes at 6801. Check after the run:
`SELECT parcel_id, leg_no, count(*) FROM leg GROUP BY 1, 2 HAVING count(*) > 1` returns nothing.
