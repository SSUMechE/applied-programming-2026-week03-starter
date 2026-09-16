"""Verify the Week 3 environment without executing student TODO bodies."""

from __future__ import annotations

import importlib
import importlib.metadata
import sys
from pathlib import Path


EXPECTED_PYTHON = (3, 12)
REQUIRED_DISTRIBUTIONS = {
    "numpy": "2.5.1",
    "pytest": "9.1.1",
    "setuptools": "83.0.0",
    "build": "1.3.0",
}
PUBLIC_NAMES = (
    "PlanningModelError",
    "Configuration",
    "ConfigurationBounds",
    "Path",
    "PlanningProblem",
    "PlanResult",
    "PlanningRun",
)


def check_environment() -> list[str]:
    failures: list[str] = []
    if sys.version_info[:2] != EXPECTED_PYTHON:
        failures.append(
            "Python must be 3.12.x; current interpreter is "
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    for distribution, expected_version in REQUIRED_DISTRIBUTIONS.items():
        try:
            version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            failures.append(f"missing distribution: {distribution}")
        else:
            if version != expected_version:
                failures.append(
                    f"{distribution} must be {expected_version}; current version is {version}"
                )
            else:
                print(f"[OK] {distribution} {version}")

    try:
        package = importlib.import_module("ap_week03_planning")
    except Exception as exc:  # pragma: no cover - diagnostic path
        failures.append(f"cannot import ap_week03_planning: {type(exc).__name__}: {exc}")
    else:
        loaded = Path(package.__file__).resolve()
        expected = Path(__file__).resolve().parents[1] / "src" / "ap_week03_planning" / "__init__.py"
        if loaded != expected.resolve():
            failures.append(f"ap_week03_planning must load this repository's editable source, not {loaded}")
        else:
            print(f"[OK] ap_week03_planning import: {loaded}")
        for name in PUBLIC_NAMES:
            if not hasattr(package, name):
                failures.append(f"missing public object: {name}")
    return failures


def main() -> int:
    print(
        "[INFO] Python",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )
    failures = check_environment()
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Week 3 object-programming environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
