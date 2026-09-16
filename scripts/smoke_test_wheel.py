"""Import the installed wheel and exercise a minimal valid object graph."""

from __future__ import annotations

import importlib.metadata
import json
from pathlib import Path

import ap_week03_planning
from ap_week03_planning import Configuration, ConfigurationBounds, PlanningProblem


def main() -> int:
    distribution = importlib.metadata.distribution("ap-week03-planning")
    direct_url = json.loads(distribution.read_text("direct_url.json") or "{}")
    if direct_url.get("dir_info", {}).get("editable"):
        raise RuntimeError("wheel smoke test requires a non-editable wheel installation")
    installed_root = Path(distribution.locate_file("")).resolve()
    loaded = Path(ap_week03_planning.__file__).resolve()
    if not loaded.is_relative_to(installed_root):
        raise RuntimeError(f"package did not load from its installed distribution: {loaded}")
    print(f"[INFO] installed distribution import: {loaded}")
    bounds = ConfigurationBounds(Configuration((0.0, 0.0)), Configuration((2.0, 2.0)))
    problem = PlanningProblem("wheel-smoke", Configuration((0.0, 0.0)), Configuration((1.0, 1.0)), bounds)
    assert problem.problem_id == "wheel-smoke"
    print("[PASS] installed Week 3 wheel created a valid PlanningProblem.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
