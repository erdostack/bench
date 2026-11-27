"""Case-local helpers for the round-8 (qr8-f) Cypher cases of query-review (a copy in each case folder that uses
it). Built on casekit, r4kit and wkit (copied from round 7; wkit carries the qr8-f additions listed in its
docstring). Everything here is structural; nothing grades wording.

    type_mix(text, typed)       comparisons that Cypher evaluates to null because the two sides have different
                                types: a property stored as DATETIME or DATE compared with a string literal or
                                with another temporal type, or a STRING property compared with a temporal value.
                                typed = {property name: "datetime" | "date" | "string"}. Converting the property
                                first (datetime(x.p) < ..., date(x.p) < ...) is not flagged.
    uses_apoc(text)             the text calls an apoc.* procedure or function
    calls(chunk)                [(imported variables, rows per transaction or None, body text)] for every
                                CALL { } IN TRANSACTIONS of a statement; rows is 1000 (Neo4j's default) when
                                no OF n ROWS is given, None when the size is not a literal
    batch_of(chunk, var)        (imported variables, rows) of the CALL ... IN TRANSACTIONS whose body deletes or
                                writes `var`, or None when the write is not inside one
    creates_rel(chunk, rel_type)
                                [(start variable, end variable)] of every CREATE / MERGE of a relationship of
                                that type, written in either arrow direction (normalised to start -> end)
    plan_or_read(statement)     EXPLAIN, or a statement with no write clause
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import casekit as ck  # noqa: E402
from casekit import cl  # noqa: E402

OPS = r"(?:<=|>=|<>|=|<|>)"
TEMPORAL = ("datetime", "date", "localdatetime", "localtime", "time")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", cl.strip_comments(text))


def type_mix(text: str, typed: dict[str, str]) -> list[str]:
    flat = _flat(text)
    out = []
    for prop, kind in typed.items():
        p = re.escape(prop)
        left = rf"\b\w+\s*\.\s*{p}\b(?!\s*\.)\s*{OPS}\s*"          # x.prop <op> ...
        right = rf"\s*{OPS}\s*\w+\s*\.\s*{p}\b(?!\s*\.)"           # ... <op> x.prop
        if kind in ("datetime", "date"):
            if re.search(left + r"['\"]", flat) or re.search(r"['\"]" + right, flat):
                out.append(f"compares {prop} (stored as {kind.upper()}) with a string: null in Cypher, selects nothing")
            others = [f for f in TEMPORAL if f != kind]
            fn = r"(?<![\w.])(?:" + "|".join(others) + r")\s*(?:\.\w+\s*)?\("
            if re.search(left + fn, flat, re.I) or re.search(fn + r"[^()]*\)" + right, flat, re.I):
                out.append(f"compares {prop} (stored as {kind.upper()}) with another temporal type: null in Cypher")
        elif kind == "string":
            fn = r"(?<![\w.])(?:" + "|".join(TEMPORAL) + r")\s*(?:\.\w+\s*)?\("
            if re.search(left + fn, flat, re.I) or re.search(fn + r"[^()]*\)" + right, flat, re.I):
                out.append(f"compares {prop} (stored as STRING) with a temporal value: null in Cypher, selects nothing")
    return out


def uses_apoc(text: str) -> bool:
    return bool(re.search(r"\bapoc\s*\.", cl.strip_comments(text), re.I))


def _match_brace(s: str, i: int) -> int:
    """Index of the brace closing the one at s[i] (strings skipped)."""
    depth, j, q = 0, i, None
    while j < len(s):
        c = s[j]
        if q:
            if c == q:
                q = None
        elif c in "'\"`":
            q = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def calls(chunk: str):
    s = cl.strip_comments(chunk)
    out = []
    for m in re.finditer(r"\bCALL\s*(\(([^()]*)\))?\s*\{", s, re.I):
        open_at = m.end() - 1
        close = _match_brace(s, open_at)
        if close < 0:
            continue
        body = s[open_at + 1:close]
        tail = s[close + 1:]
        t = re.match(r"\s*IN\s+(?:\d+\s+)?(?:CONCURRENT\s+)?TRANSACTIONS\b(?:\s+OF\s+(\S+)\s+ROWS?\b)?", tail, re.I)
        if not t:
            continue
        if m.group(1) is not None:
            names = {x.strip() for x in m.group(2).split(",") if x.strip()}
            if names == {"*"}:
                names = {"*"}
        else:
            w = re.match(r"\s*WITH\s+(.*?)(?=\b(?:MATCH|OPTIONAL|WHERE|DELETE|DETACH|SET|REMOVE|CREATE|MERGE|CALL|WITH|UNWIND|RETURN|FOREACH)\b)",
                         body, re.I | re.S)
            names = set()
            if w:
                for item in w.group(1).split(","):
                    a = re.search(r"\bAS\s+(\w+)\s*$", item.strip(), re.I)
                    names.add(a.group(1) if a else item.strip())
        size = t.group(1)
        rows = 1000 if size is None else (int(size) if size.isdigit() else None)
        out.append((names, rows, body))
    return out


def batch_of(chunk: str, var: str):
    for names, rows, body in calls(chunk):
        if re.search(rf"\b(?:DETACH\s+)?DELETE\b[^;]*\b{re.escape(var)}\b", body, re.I) or \
                re.search(rf"\b(?:SET|REMOVE|CREATE|MERGE)\b[^;]*\b{re.escape(var)}\b", body, re.I):
            return names, rows
    return None


def creates_rel(chunk: str, rel_type: str):
    out = []
    t = re.escape(rel_type)
    for w in ck.writes(chunk):
        if w.kw not in ("CREATE", "MERGE"):
            continue
        txt = re.sub(r"\s+", " ", w.text)
        for m in re.finditer(rf"\(\s*(\w+)\s*(?::\w+\s*)*\)\s*-\s*\[\s*\w*\s*:\s*`?{t}`?[^\]]*\]\s*-\s*>\s*\(\s*(\w+)\s*(?::\w+\s*)*\)", txt):
            out.append((m.group(1), m.group(2)))
        for m in re.finditer(rf"\(\s*(\w+)\s*(?::\w+\s*)*\)\s*<\s*-\s*\[\s*\w*\s*:\s*`?{t}`?[^\]]*\]\s*-\s*\(\s*(\w+)\s*(?::\w+\s*)*\)", txt):
            out.append((m.group(2), m.group(1)))
    return out


def plan_or_read(statement: str) -> bool:
    return ck.is_plan_only(statement) or not ck.is_write(statement)
