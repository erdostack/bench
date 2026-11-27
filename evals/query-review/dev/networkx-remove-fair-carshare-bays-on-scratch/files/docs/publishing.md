# Publishing a change

A change to `published` is a script `changes/NNNN_<slug>.py` (it runs with `G` bound), reviewed in a PR and
run by the fleet planner with `bin/gx published changes/<file>.py`. Nobody edits published by hand.

None of this applies to `scratch`.
