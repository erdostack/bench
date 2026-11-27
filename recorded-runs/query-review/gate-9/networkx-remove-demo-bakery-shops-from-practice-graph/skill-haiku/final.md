The 12 DEMO- training shops are gone from the practice graph, with their links. The practice graph is now 425 nodes and 433 edges, down from 437 and 445.

Removed: DEMO-01 to DEMO-12, and the 12 `delivers` edges from depots to them. Nothing else changed: the five depots and the real shops, their edges and their attributes are as they were. The network graph was not touched.

The change is in `changes/remove_demo_shops.py`. I ran it on a copy first and then on the practice graph, through `bin/net practice`. A second run changes nothing. The practice graph has no production role (`docs/network.md`), so there is no review or hand-back step.

One thing to know: `bin/new-practice` rebuilds the practice graph from the network and adds the twelve DEMO- shops again. If anyone runs it before the next training, the shops come back. The change script needs to run again after that.
