# Archiving work orders

The work-order app lists `:WorkOrder:Active` nodes. Archiving an order means adding the label `:Archived` and
removing `:Active`. The order keeps its properties and its `ON_ASSET` relationship (the regulator returns and
the asset history still read archived orders); nothing is deleted.
