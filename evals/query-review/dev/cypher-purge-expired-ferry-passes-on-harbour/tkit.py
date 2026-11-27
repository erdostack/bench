"""Case-local helper (round 8, qr8-i): temporal type checks that the sample evaluator in wkit cannot make.

wkit evaluates temporal values as ISO text, so it cannot see that Neo4j compares values of different types
as null: a STRING property compared with date(...) or datetime(...), a DATE or DATETIME property compared
with a string literal, or a DATE compared with a DATETIME selects nothing. The fixture's docs say which type
each temporal property has; `mismatches(text, types)` lists every ordering or equality comparison in the
text where a property named in `types` meets an operand of another type.

    types = {"closedOn": "date", "raisedAt": "datetime", "liveSince": "string"}

Recognised operands: a string literal (STRING), a call of date / datetime / localdatetime / localtime /
time (that type), a temporal call followed by `+` or `-` a duration (the call's type). A property wrapped in
a conversion call (`date(c.liveSince)`) is not a bare property and is not checked: converting first is the
right fix. Parameters and anything else are not judged.
"""
from __future__ import annotations

import sys
from pathlib import Path

CASE = Path(__file__).resolve().parent
sys.path.insert(0, str(CASE.parents[1] / "lib"))
import cypher_lint as cl  # noqa: E402

CMP = {"<", ">", "<=", ">=", "=", "<>"}
TEMPORAL = {"date": "date", "datetime": "datetime", "localdatetime": "localdatetime", "localtime": "localtime",
            "time": "time"}


def _match_open(toks, close_i):
    depth = 0
    for j in range(close_i, -1, -1):
        if toks[j].text == ")":
            depth += 1
        elif toks[j].text == "(":
            depth -= 1
            if depth == 0:
                return j
    return None


def _match_close(toks, open_i):
    depth = 0
    for j in range(open_i, len(toks)):
        if toks[j].text == "(":
            depth += 1
        elif toks[j].text == ")":
            depth -= 1
            if depth == 0:
                return j
    return None


def _right_type(toks, i):
    """Type of the operand starting at token i, or None when unknown."""
    if i >= len(toks):
        return None
    t = toks[i]
    if t.kind == "string":
        return "string"
    if t.kind == "ident" and t.text.lower() in TEMPORAL and i + 1 < len(toks) and toks[i + 1].text == "(":
        return TEMPORAL[t.text.lower()]
    if t.kind == "ident" and t.text.lower() in TEMPORAL and i + 3 < len(toks) and toks[i + 1].text == "." \
            and toks[i + 2].text.lower() == "truncate" and toks[i + 3].text == "(":
        return TEMPORAL[t.text.lower()]                 # QA qr9x-2: date.truncate(...) is a DATE
    return None


def _left_type(toks, i):
    """Type of the operand ending at token i, or None."""
    if i < 0:
        return None
    t = toks[i]
    if t.kind == "string":
        # a string that is itself an argument of a call is not the operand
        return "string" if not (i > 0 and toks[i - 1].text == "(") else None
    if t.text == ")":
        j = _match_open(toks, i)
        if j is None or j == 0:
            return None
        f = toks[j - 1]
        if f.text.lower() == "truncate" and j >= 3 and toks[j - 2].text == "." and toks[j - 3].text.lower() in TEMPORAL:
            return TEMPORAL[toks[j - 3].text.lower()]   # QA qr9x-2
        if f.kind == "ident" and f.text.lower() in TEMPORAL:
            return TEMPORAL[f.text.lower()]
        if f.kind == "ident" and f.text.lower() == "duration":
            # <temporal call> +/- duration(...) : the type of the temporal call
            if j - 2 >= 0 and toks[j - 2].text in ("+", "-"):
                return _left_type(toks, j - 3)
    return None


def mismatches(text: str, types: dict[str, str]) -> list[str]:
    toks = cl.tokenize(cl.strip_comments(text))
    out = []
    for i in range(len(toks) - 2):
        a, dot, p = toks[i], toks[i + 1], toks[i + 2]
        if a.kind not in ("ident", "bident") or dot.text != "." or p.kind not in ("ident", "bident"):
            continue
        name = p.text.strip("`")
        if name not in types:
            continue
        if i + 3 < len(toks) and toks[i + 3].text in (".", "("):
            continue                                    # c.liveSince.year, or a method-like call
        want = types[name]
        other = None
        if i + 3 < len(toks) and toks[i + 3].kind == "op" and toks[i + 3].text in CMP:
            other = _right_type(toks, i + 4)
        elif i - 1 >= 0 and toks[i - 1].kind == "op" and toks[i - 1].text in CMP:
            other = _left_type(toks, i - 2)
        if other is None or other == want:
            continue
        out.append(f"{a.text}.{name} ({want.upper()}) compared with a {other.upper()} value: null in Cypher, selects nothing")
    return out
