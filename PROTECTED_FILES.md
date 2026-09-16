# Protected files and frozen public contract

Students may manually edit only:

- `src/ap_week03_planning/domain.py`
- `src/ap_week03_planning/history.py`
- `tests/test_student_evidence.py`
- `artifacts/engineering_note.md`

Do not edit:

- `src/ap_week03_planning/__init__.py`
- `src/ap_week03_planning/geometry.py`
- `src/ap_week03_planning/demo.py`
- `src/ap_week03_planning/visualize.py`
- every file under `scripts/`
- `tests/test_published_contract.py`
- `pyproject.toml`, `requirements.txt`, and `environment.yml`
- every file under `docs/`
- `README.md`, `.gitignore`, and this protected-file list

Protected commands create or replace these required generated outputs. Commit
them, but do not hand-edit them:

- `artifacts/planning_objects_report.json`
- `artifacts/planning_objects_preview.svg`
- one `dist/ap_week03_planning-*.whl`

The wheel build may also create ignored `build/` and `src/*.egg-info/`
directories. These are build by-products, not additional editable source.

Within `domain.py` and `history.py`, keep the public class names, field names,
method names, public error type, documented meanings, and TODO numbering. You
may add private helpers whose names begin with `_`.

`Configuration`, `ConfigurationBounds`, `Path`, `PlanningProblem`, and
`PlanResult` are frozen value objects. `PlanningRun` is the one mutable state
owner. Invalid public construction or update must raise `PlanningModelError`.
Do not silently clip, reshape, pad, truncate, or repair invalid data.

`geometry.py` is the supplied pure numerical boundary. The demo and SVG caller
show the object data that your package created; they do not implement a motion
planner, collision checker, controller, or physics simulation.

