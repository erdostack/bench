Position: switch

Good call. A path column turns descendants into an indexed prefix scan and removes the recursion entirely; moves will
need an UPDATE of the subtree, which is fine.
