The ADR holds: 310,000 tables and 1.9 million edges fit easily in a 4 GiB pod, and the SQL is clearly too slow (44% cancelled). Go ahead with the loader. Decision: in-process-library.
