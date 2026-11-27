Added sql/one_stop.sql.

It joins `flight` to itself on the connecting airport: the first leg leaves :origin on :day (UTC), the second
leaves for :dest at least 50 minutes and at most 5 hours after the first lands, the window revenue management set
(docs/graph/DECISION.md). One stop only, so there is no recursion.
