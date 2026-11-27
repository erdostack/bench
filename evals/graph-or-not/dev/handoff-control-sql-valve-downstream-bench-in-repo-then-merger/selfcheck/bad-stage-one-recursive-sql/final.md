Still stands: yes

docs/slo.md says 1 s p95, and to revisit when p95 passes 600 ms or the process passes 6 GB of the 8 GB pod. The
networkx walk went from 0.21 s to 0.38 s and from 1.9 GB to 3.3 GB: both inside the lines. The recursive query went
from 5.2 s to 9.4 s, so going back is even less of an option.
