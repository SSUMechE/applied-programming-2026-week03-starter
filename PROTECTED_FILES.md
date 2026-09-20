# Files you edit

Edit only these three files:

- `src/ap_week03_planning/domain.py`: TODO 1–7.
- `src/ap_week03_planning/history.py`: TODO 8.
- `tests/test_student_evidence.py`: your independent tests.

Keep the public class names, field names, method names, signatures, decorators,
error type and TODO numbers. You may add private helpers named with a leading
underscore. The numerical functions and `PlanningRun._results` field are provided.

`Configuration`, `ConfigurationBounds`, `Path`, `PlanningProblem` and
`PlanResult` are frozen value objects. `PlanningRun` owns mutable result history.
Invalid construction or updates raise `PlanningModelError`. Do not clip,
reshape, pad, truncate or silently repair invalid data.

All other supplied files are protected, including public tests, scripts,
installation files, documentation and the provided modules. The Assignment
submits code and tests. The chapter's visualization tools are retained for
Reading Section 6 and are not part of the Assignment workflow.
