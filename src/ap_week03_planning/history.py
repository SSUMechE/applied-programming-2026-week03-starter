"""The single mutable state owner completed in the Week 3 Assignment."""

from __future__ import annotations

from dataclasses import dataclass, field

from .domain import PlanResult, PlanningModelError, PlanningProblem


@dataclass
class PlanningRun:
    """Own the ordered results recorded for one planning problem."""

    problem: PlanningProblem
    _results: list[PlanResult] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        # TODO 8: require a PlanningProblem. The per-run _results list is provided.
        raise NotImplementedError("TODO 8: validate PlanningRun")

    def record_result(self, result: PlanResult) -> None:
        """Append a compatible result or leave this run unchanged."""
        # TODO 8: validate result type/problem before append. Reject without changes.
        raise NotImplementedError("TODO 8: implement PlanningRun.record_result")

    @property
    def results(self) -> tuple[PlanResult, ...]:
        """Return an immutable snapshot of the current result history."""
        # TODO 8: return a tuple of the current entries, not the mutable list.
        raise NotImplementedError("TODO 8: implement PlanningRun.results")

    @property
    def latest(self) -> PlanResult | None:
        """Return the most recently recorded result, or None when empty."""
        # TODO 8: return the last result, or None if no result has been recorded.
        raise NotImplementedError("TODO 8: implement PlanningRun.latest")

