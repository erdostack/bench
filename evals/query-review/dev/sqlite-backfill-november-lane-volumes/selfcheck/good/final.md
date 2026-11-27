Wrote jobs/backfill_lanes.py. It finds the days in box_legs that lane_days doesn't list yet (4-22 November;
1-3 November are already in lanes) and adds them one day per transaction with the nightly job's own
function, so each day's lane updates and its lane_days row commit together. A day touches about 1,400
lanes, under the 2,000-row limit. If the scheduler kills it and starts it again, it skips the days that
already committed, so nothing is counted twice. Check before and after with
`SELECT count(*), sum(legs) FROM lane_days`.
