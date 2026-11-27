Added page_order(conn, policy_id) to oncall/escalate.py. It follows escalates_to from the given policy until
there is no next policy, and stops if the chain loops back to a policy already in the list, so it always
terminates.
