# Model lifecycle

A model is `current` while it can be ordered for new sites. When the vendor withdraws it, it becomes
`retired`: the design tool stops offering it for new designs.

A retired model is removed from the catalogue only once nothing refers to it any more: no installed antenna
(`antennas.model_id`) and no spare stock at any depot (`spares.model_code`, which holds the model's code).
Until then the maintenance app and the depot pick lists still need its row.
