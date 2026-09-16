"""Run and verify the intentional Week 3 starter baseline."""

from __future__ import annotations

import re
import subprocess
import sys


EXPECTED_FAILED = 68
EXPECTED_PASSED = 8


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "--tb=no",
        "tests/test_published_contract.py",
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    match = re.search(r"(\d+) failed, (\d+) passed", output)
    if match is None:
        print("[FAIL] Could not read the pytest baseline summary.")
        return 1
    failed, passed = map(int, match.groups())
    if (failed, passed) != (EXPECTED_FAILED, EXPECTED_PASSED):
        print(
            f"[FAIL] Unexpected baseline: {failed} failed, {passed} passed; "
            f"expected {EXPECTED_FAILED} failed, {EXPECTED_PASSED} passed."
        )
        return 1
    print(f"[PASS] Intentional baseline confirmed: {failed} failed, {passed} passed.")
    print("[INFO] Record the summary and first FAILED node ID in the engineering note.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

