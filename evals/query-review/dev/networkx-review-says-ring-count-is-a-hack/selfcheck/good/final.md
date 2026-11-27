I'd not make this change; the formula is the ring count, and simple_cycles isn't.

- docs/descriptors.md defines ring_count as the size of the smallest set of smallest rings, which for any molecule
  is bonds - atoms + fragments. That's what the function computes (the cycle rank of the graph).
- `nx.simple_cycles` lists every closed path, not every ring. Two fused six-membered rings have 3 closed paths (each
  ring, plus the outer ten-membered loop), the eight-atom cube cage has 28, and a flat flake of 12 rings has
  1,692. On data/molecules.json the simple-cycle count differs from the documented value for 113 of 145
  molecules; the formula matches all of them.

Suggested reply to the reviewer with those numbers. No code change.
