`trapped_junctions(conn)` in `oneway/trapped.py` already contains the rewrite we decided on, and I found nothing that needed changing, so I left the file as it was. It returns the sorted list of junction ids the draft traps. The signature is unchanged, and `oneway/report.py` still calls it as before.

How it works: it builds a directed graph from the `mode = 'road'` segments only, honouring `oneway` (0 two-way, 1 a to b, -1 b to a). It treats the whole ring road as one virtual node. A road junction off the ring is trapped if it cannot reach the ring or cannot be reached from it. There is no step limit, and footpaths are ignored.

I ran it on a small hand-built draft. These cases came out as expected:
- A 60-junction one-way loop through the ring is not flagged.
- A junction you can enter but not leave is flagged.
- A junction you can leave but not enter is flagged.
- A junction on footpaths only is not reported.
- A junction with no segments at all is not reported.

I have not run it on a real draft file, because none is in the checkout. Run `python -m oneway.report var/<draft>.db` on yours to see the real count. If a draft has no ring junction on any road, every road junction is reported, since none can reach the ring. I added no test files.
