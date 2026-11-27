One thing has to be fixed before the hand-over, and it is a wrong-answer bug, not a style point.

The README says the writes keep Parcel.depot_code in step with the AT relationship. register_parcel does. move_parcel does not: it deletes the old AT, creates the new one, sets the status and leaves depot_code alone. Since the dispatch screen (depot_backlog) reads depot_code, every parcel that has moved is listed at the depot that first received it and is missing from the depot it is really at. That is roughly 70% of parcels.

Fix is one line in move_parcel plus a one-off repair; both are in docs/graph/ROAST.md and findings.json, with two low notes.
