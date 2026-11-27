-- RW-140: waiting-times report. Filled by jobs/backfill_wait_days.py.
ALTER TABLE referrals ADD COLUMN wait_days INTEGER;
