"""Case-local helper (round 9, qr9-a): run the SET / REMOVE writes of a change file, statement by statement in
order, on sample nodes, and report each sample's end state. A copy lives in each case folder that uses it.

    simulate(statements, samples, params=None) -> (states, problems)

`statements` are plain statements (read through qa8xnorm.statements first). `samples` is
[(name, node)], node = {"labels": set, "props": dict}. For each writing statement the sample is selected
(wkit.selects on the statement's restrictions of the written variable, against the sample's state before the
statement: Cypher matches first, then writes) and then every SET and REMOVE item on that variable is applied:
`v:A:B` adds or removes labels, `v.p = expr` sets a property to the value of expr evaluated on the sample's
state before the statement (null removes it, as in Cypher), `v += {k: expr}` sets each key, `v.p` in REMOVE
removes it. Anything else that writes (DELETE, CREATE, MERGE, a write on another variable, `v = {...}`) is
reported in `problems`, as is anything the evaluator cannot read.
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

CASE = Path(__file__).resolve().parent
sys.path.insert(0, str(CASE))
import casekit as ck  # noqa: E402
import r4kit as rk  # noqa: E402
import wkit as wk  # noqa: E402
from casekit import cl  # noqa: E402

LABELS = re.compile(r"^(\w+)((?::`?\w+`?)+)$")
PROP = re.compile(r"^(\w+)\.(\w+)$")


def _items(clause):
    return [it for it in cl._split_top(clause.toks, ",") if it]


def _parse_item(kw, item):
    """('labels', var, [labels]) | ('prop', var, key, expr_toks) | ('merge', var, map_toks) | ('unprop', var, key)"""
    flat = "".join(t.text for t in item)
    m = LABELS.match(flat)
    if m:
        return ("labels", m.group(1), [x.strip("`") for x in m.group(2).split(":")[1:]])
    if kw == "REMOVE":
        m = PROP.match(flat)
        if m:
            return ("unprop", m.group(1), m.group(2))
        raise wk.Unsupported(f"REMOVE {flat}")
    texts = [t.text for t in item]
    if len(item) >= 4 and item[1].text == "." and item[3].text == "=" and item[0].kind in ("ident", "bident"):
        return ("prop", item[0].name, item[2].name if hasattr(item[2], "name") else item[2].text, item[4:])
    if len(item) >= 3 and item[0].kind in ("ident", "bident") and texts[1] == "+" and texts[2] == "=":
        return ("merge", item[0].name, item[3:])
    if len(item) >= 2 and item[0].kind in ("ident", "bident") and texts[1] == "+=":
        return ("merge", item[0].name, item[2:])
    raise wk.Unsupported(f"{kw} {flat}")


def writes_of(chunk):
    """[(kw, parsed item)] for every SET / REMOVE item; raises Unsupported for any other write."""
    out = []
    for kw, flat, clause in wk.statement_writes(chunk):
        if kw not in ("SET", "REMOVE"):
            raise wk.Unsupported(f"{kw} {flat[:60]}")
        for item in _items(clause):
            out.append((kw, _parse_item(kw, item)))
    return out


def _apply(state, before, kw, w, named, params):
    kind, var = w[0], w[1]
    env = {var: before}
    if kind == "labels":
        if kw == "SET":
            state["labels"] |= set(w[2])
        else:
            state["labels"] -= set(w[2])
    elif kind == "unprop":
        state["props"].pop(w[2], None)
    elif kind == "prop":
        val = wk.evaluate(wk.parse_expr(w[3]), env, params)
        if val is None:
            state["props"].pop(w[2], None)
        else:
            state["props"][w[2]] = val
    elif kind == "merge":
        mp = wk.evaluate(wk.parse_expr(w[2]), env, params)
        if not isinstance(mp, dict):
            raise wk.Unsupported("+= of a non-map")
        for k, v in mp.items():
            if v is None:
                state["props"].pop(k, None)
            else:
                state["props"][k] = v


def simulate(statements, samples, params=None):
    params = params or {}
    states = {name: copy.deepcopy({"labels": set(n["labels"]), "props": dict(n["props"])}) for name, n in samples}
    problems = []
    for chunk in statements:
        if not ck.is_write(chunk) or ck.is_plan_only(chunk):
            continue
        try:
            ws = writes_of(chunk)
        except wk.Unsupported as exc:
            problems.append(f"writes something other than labels and properties of the selected nodes: {exc}")
            continue
        named = rk.name_anonymous(rk.inline_leading_with(chunk))
        for name, _n in samples:
            before = copy.deepcopy(states[name])
            chosen = {}
            for _kw, w in ws:
                var = w[1]
                if var not in chosen:
                    try:
                        chosen[var] = wk.selects(named, var, before, params)
                    except wk.Unsupported as exc:
                        problems.append(f"could not evaluate the predicate on {var}: {exc}")
                        chosen[var] = False
            for kw, w in ws:
                if chosen.get(w[1]):
                    try:
                        _apply(states[name], before, kw, w, named, params)
                    except wk.Unsupported as exc:
                        problems.append(f"could not evaluate {kw} on {w[1]}: {exc}")
    return states, list(dict.fromkeys(problems))
