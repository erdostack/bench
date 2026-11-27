Position: keep

We decided on in-process-library: load the variant into networkx in the viewer. Numbers: today's trace is
~600 queries / 2.1 s; in memory it's 0.4 ms after a 90 ms load, 45 MB for the biggest variant, data changes
once a month. A graph database doesn't beat 0.4 ms; it adds a system to run.
