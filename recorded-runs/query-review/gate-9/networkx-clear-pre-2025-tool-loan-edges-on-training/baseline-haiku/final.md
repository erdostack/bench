Done. I removed the borrowed edges for loans that went out before 1 January 2025 from the training graph. Nothing else changed.

- Removed 1,203 `borrowed` edges with `on` before 2025-01-01. 1,200 borrowed edges remain.
- All 301 members, all 220 tools and the 4 branches are still there, as are the 260 reservations and the 220 `kept_at` edges.
- Members who had only pre-2025 loans now have no edges. FM-0999 is one of them and is still in the graph. FM-0007 and FM-0008 keep their 2025-and-later loans.
- The catalogue graph (data/catalogue.graphml) was not touched.

The change script is at work/purge_borrowed_pre2025.py, and the graph is saved as data/training.graphml. It is rebuilt from the fixed seed with scripts/build_training.py if you want a clean copy again.
