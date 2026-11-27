affected_by_repeal is now one recursive query over amends and depends_on references (citations don't carry
a repeal, per the decision record), with no depth limit. UNION stops it revisiting a bylaw, so a loop in the
references would still end.
