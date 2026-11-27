#!/usr/bin/env python3
"""check_mirror.py REPO_ID | --selftest

Fail if the dataset REPO_ID on the Hugging Face Hub and the files git tracks here are not the same set of
paths. The sync workflow runs this after every upload, so a file the upload tool skips cannot go unnoticed.

Left out of the comparison on purpose:
- this repository's own git and CI files at the root (.gitattributes, .gitignore, .github/), which the sync
  does not upload;
- the Hub's own .gitattributes, which the Hub writes.

It compares paths, not contents. With --selftest it checks its own comparison and touches no network.
"""
import subprocess
import sys


def uploaded(paths):
    """The tracked paths the sync uploads: everything except what starts with .git at the root."""
    return {p for p in paths if p and not p.startswith(".git")}


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True).stdout
    return uploaded(out.decode("utf-8").split("\0"))


def compare(local, remote):
    """Return (missing on the Hub, only on the Hub), each sorted."""
    remote = {p for p in remote if p != ".gitattributes"}
    return sorted(set(local) - remote), sorted(remote - set(local))


def selftest():
    local = uploaded([".gitattributes", ".gitignore", ".github/workflows/sync-to-hub.yml", "README.md",
                      "evals/a/dev/c/files/.github/workflows/ci.yml", "evals/a/dev/c/files/.gitignore", ""])
    assert local == {"README.md", "evals/a/dev/c/files/.github/workflows/ci.yml", "evals/a/dev/c/files/.gitignore"}
    assert compare(local, local | {".gitattributes"}) == ([], [])
    assert compare(local, {"README.md", ".gitattributes"}) == (
        ["evals/a/dev/c/files/.github/workflows/ci.yml", "evals/a/dev/c/files/.gitignore"], [])
    assert compare(local, local | {"stale.txt"}) == ([], ["stale.txt"])
    print("check_mirror selftest: ok")
    return 0


def main(argv):
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) != 2:
        print(__doc__)
        return 2
    from huggingface_hub import HfApi  # only needed for the real check

    local = tracked()
    remote = set(HfApi().list_repo_files(argv[1], repo_type="dataset"))
    missing, extra = compare(local, remote)
    print(f"{len(local)} files to mirror, {len(remote)} on the Hub; "
          f"missing on the Hub: {len(missing)}; only on the Hub: {len(extra)}")
    for label, paths in (("missing on the Hub", missing), ("only on the Hub", extra)):
        for path in paths[:50]:
            print(f"  {label}: {path}")
        if len(paths) > 50:
            print(f"  ... and {len(paths) - 50} more {label}")
    return 1 if missing or extra else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
