# Service contracts

A device goes under a service contract only if it is ours and in use or kept as a spare (`in_service`
or `in_store`). Never add cover for:

- `loan` devices: the lender's own agreement covers them, and we are invoiced if we add them to ours;
- `condemned` devices: they are waiting for disposal.

A device has at most one `covered_by` edge to a given contract. When a contract starts early for a
pilot ward, those devices already have their edge; do not add a second one.
