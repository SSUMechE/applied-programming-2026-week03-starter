"""Create and print one deterministic object-collaboration example."""

from __future__ import annotations

from .domain import Configuration, ConfigurationBounds, Path, PlanResult, PlanningProblem
from .history import PlanningRun


def build_demo_run() -> PlanningRun:
    bounds = ConfigurationBounds(Configuration((0.0, 0.0)), Configuration((4.0, 3.0)))
    problem = PlanningProblem(
        "demo-tool-path",
        Configuration((0.0, 0.0)),
        Configuration((3.2, 2.0)),
        bounds,
    )
    path = Path(
        (
            problem.start,
            Configuration((1.0, 1.4)),
            Configuration((2.4, 1.1)),
            problem.goal,
        )
    )
    run = PlanningRun(problem)
    run.record_result(PlanResult(problem, path, "validated supplied path"))
    return run


def main() -> None:
    run = build_demo_run()
    result = run.latest
    assert result is not None and result.path is not None
    print(f"problem_id: {run.problem.problem_id}")
    print(f"configuration dimension: {run.problem.start.dimension}")
    print(f"waypoints: {len(result.path.waypoints)}")
    print(f"path length: {result.path.length():.6f}")
    print(f"result count: {len(run.results)}")
    print(f"succeeded: {result.succeeded}")


if __name__ == "__main__":
    main()

