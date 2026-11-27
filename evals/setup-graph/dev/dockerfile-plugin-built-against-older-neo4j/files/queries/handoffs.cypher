// Cheapest hand-off chain between two depots, using the server-side procedure.
CALL parcel.handoffs($from, $to, 6) YIELD from, to, cost
RETURN from, to, cost;
