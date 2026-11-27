I have not applied the backfill to core. I wrote it as changes/0042_backfill_home_centre.py and rehearsed it on the rehearsal copy. The donor-systems on-call applies it to core with `bin/apply core changes/0042_backfill_home_centre.py` after review.

What it does: for each active donor who has given and has no home_centre, it adds one, set to the centre of their most recent donation with that donation's day. This is the rule in docs/model.md. It commits 500 rows at a time, as docs/changes.md requires, and running it again adds nothing.

Rehearsal result: 4,300 home_centre edges added, and a second run added none. Afterwards every active donor who has given has exactly one home_centre, no donor has two, and each one's day and centre match their latest donation. Total home_centre edges went from 1,850 to 6,150.

Two things to check before it goes to core:

- The request said every donor who has given. The model only gives a home_centre to active donors, and withdrawn donors are meant to have none. 855 withdrawn donors who have given are therefore left without one. If the booking app should show them too, the model needs changing first; I did not change it.
- 461 existing home_centre edges point at a centre other than the donor's latest donation. The change never touches a home_centre that already exists, so these are kept as they are. They are probably donors whom donor care set by hand after a move. Nothing was done to them.
