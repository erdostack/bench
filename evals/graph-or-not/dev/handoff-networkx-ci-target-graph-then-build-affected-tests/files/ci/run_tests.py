"""Run test targets for a pipeline. Today: every test target, on every PR."""
import json
import subprocess
import sys


def all_tests(graph):
    return sorted(name for name, t in graph["targets"].items() if t["kind"] == "test")


def main(graph_path="var/graph.json"):
    graph = json.load(open(graph_path))
    tests = all_tests(graph)  # TODO: on PRs, only the tests affected by the change
    sys.exit(subprocess.call(["buildtool", "test", *tests]))


if __name__ == "__main__":
    main(*sys.argv[1:])
