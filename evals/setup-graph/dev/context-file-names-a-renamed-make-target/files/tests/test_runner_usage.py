import subprocess
import sys


def test_runner_prints_usage_without_arguments():
    proc = subprocess.run([sys.executable, "-m", "orchard.tools.run_query"], capture_output=True, text=True)
    assert proc.returncode != 0
