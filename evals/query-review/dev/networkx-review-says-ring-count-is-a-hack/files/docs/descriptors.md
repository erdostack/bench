# Descriptors

## ring_count

The number of rings in the molecule, as chemists count them: the size of the smallest set of smallest rings.
For any molecule this is bonds - atoms + fragments (a fragment is a connected piece, e.g. the counter-ion of
a salt). Examples from the textbook set: a six-membered ring 1, two fused six-membered rings 2, three fused in a
row 3, a cube-shaped cage of eight atoms 5, a ten-atom diamond-like cage 3, two rings joined by a single bond 2.
A ring system that shares an edge is still counted ring by ring, not by every closed path around it.

## heavy_atoms

Atoms other than hydrogen.
