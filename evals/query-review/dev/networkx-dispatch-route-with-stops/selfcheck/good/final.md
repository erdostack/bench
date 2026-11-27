fastest_route now returns (minutes, stops) or None, using Dijkstra on the run times. The old body enumerated
every simple path of up to 12 runs: on the full export (1,400 depots) a single call did not finish in 20 s,
and about two thirds of depot pairs are more than 12 runs apart, so it would have returned None or a slower
route for them. Updated the test for the new return value; all tests pass.
