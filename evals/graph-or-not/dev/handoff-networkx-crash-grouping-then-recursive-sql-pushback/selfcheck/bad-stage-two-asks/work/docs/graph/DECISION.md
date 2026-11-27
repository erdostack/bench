# Crash grouping

Decision: in-process-library

Do the grouping with networkx in the nightly job instead of the SQL loop. It is faster and needs no new server.
