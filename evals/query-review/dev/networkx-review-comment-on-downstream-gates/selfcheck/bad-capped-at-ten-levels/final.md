Addressed Dana's comment: `downstream()` now stops expanding after `MAX_LEVELS = 10`, so the traversal is bounded even when the network contains ring canals. Tests still pass.
