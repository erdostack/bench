Still stands: yes

Budget 50 ms, was 9 ms, now 380 ms. That is over budget, but 19M rows is still small for Postgres. I would
bring back the closure table and add a cache in front of the check before considering a new datastore.
