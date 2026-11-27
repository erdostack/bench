"""Builds the snapshot every SDK downloads: all flags with their rules and prerequisites, as JSON."""
import json


def build_snapshot(conn):
    flags = {}
    for key, rollout in conn.execute("SELECT key, rollout FROM flag ORDER BY key"):
        flags[key] = {"rollout": json.loads(rollout) if isinstance(rollout, str) else rollout, "requires": []}
    for flag_key, requires_key, variation in conn.execute(
            "SELECT flag_key, requires_key, variation FROM flag_prerequisite ORDER BY 1, 2"):
        flags[flag_key]["requires"].append({"flag": requires_key, "variation": variation})
    return json.dumps({"version": 3, "flags": flags}, separators=(",", ":"))
