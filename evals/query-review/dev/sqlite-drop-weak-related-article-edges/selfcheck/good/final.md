Wrote jobs/drop_weak_related.py: deletes auto edges with score < 0.35, 1,000 per commit, and returns the
number deleted (19,646 on the copy). It skips pinned edges explicitly. The related_keep_pins trigger makes
deleting a pinned edge a silent no-op, and 1,265 weak auto edges are pinned: without the filter they stay
in every batch's selection, batches shrink and the loop stops with thousands of edges left.
