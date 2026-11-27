circular_cells now walks every loop with networkx simple_cycles and flags its cells, skipping loops that
stay entirely on Loan (the decision record's exception). A cell that refers to itself is a loop of one, so
it's flagged. The existing test still passes.
