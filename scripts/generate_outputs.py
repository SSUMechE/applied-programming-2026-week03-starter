"""Generate deterministic object evidence from the public Week 3 package."""

from __future__ import annotations

import json
from pathlib import Path

from ap_week03_planning.demo import build_demo_run
from ap_week03_planning.visualize import planning_run_svg


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def main() -> int:
    run = build_demo_run()
    result = run.latest
    if result is None or result.path is None:
        raise RuntimeError("the deterministic demo did not record a successful path")
    ARTIFACTS.mkdir(exist_ok=True)
    report = {
        "problem_id": run.problem.problem_id,
        "dimension": run.problem.start.dimension,
        "start": list(run.problem.start.values),
        "goal": list(run.problem.goal.values),
        "waypoint_count": len(result.path.waypoints),
        "path_length": result.path.length(),
        "result_count": len(run.results),
        "succeeded": result.succeeded,
        "interpretation": "object collaboration output; not a planned or simulated trajectory",
    }
    report_path = ARTIFACTS / "planning_objects_report.json"
    preview_path = ARTIFACTS / "planning_objects_preview.svg"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    preview_path.write_text(planning_run_svg(run), encoding="utf-8")
    print(f"[PASS] wrote {report_path.relative_to(ROOT)}")
    print(f"[PASS] wrote {preview_path.relative_to(ROOT)}")
    print(f"[INFO] path_length={report['path_length']:.6f}; result_count={report['result_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

