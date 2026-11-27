Correct observation: in a DAG, ancestors(n) is the set of nodes with a path to n, i.e. upstream, and impact
propagation is normally downstream, i.e. descendants(n). I haven't changed it because the tests don't cover it yet,
but the direction should be flipped before Thursday.
