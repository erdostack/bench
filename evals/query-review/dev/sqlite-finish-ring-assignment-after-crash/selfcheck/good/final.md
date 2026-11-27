The crash left chunk 29 (sensors 15001-15500) in ring_members but not in member_count, so the counts are 500
short. jobs/assign_rings.py now writes each chunk and the recomputed counts in one transaction and recounts at
the start, which repairs last night's gap. Tested on a copy: returns 10,500 (the sensors still unassigned).
