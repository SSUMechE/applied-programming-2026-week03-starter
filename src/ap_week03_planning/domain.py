"""Planning-domain value objects completed in Assignment 3, Part A."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .geometry import polyline_length


ConfigurationLike = Sequence[float] | NDArray[np.generic]


class PlanningModelError(ValueError):
    """Raised when a public planning-domain invariant is violated."""


def _normalized_values(values: ConfigurationLike, *, name: str) -> tuple[float, ...]:
    """Return an owned tuple of finite real values or raise the public error."""
    # TODO 1: validate representation and values, then return owned float values.
    raise NotImplementedError("TODO 1: implement _normalized_values")


@dataclass(frozen=True)
class Configuration:
    """One configuration represented by an owned tuple of finite coordinates."""

    values: ConfigurationLike

    def __post_init__(self) -> None:
        # TODO 1: normalize values inside this frozen dataclass.
        raise NotImplementedError("TODO 1: validate Configuration")

    @property
    def dimension(self) -> int:
        """Return the number of coordinates in this configuration."""
        # TODO 2: report the normalized value count.
        raise NotImplementedError("TODO 2: implement Configuration.dimension")

    def as_array(self) -> NDArray[np.float64]:
        """Return a new float64 array; the caller may modify it safely."""
        # TODO 2: return an independent array rather than internal shared state.
        raise NotImplementedError("TODO 2: implement Configuration.as_array")


@dataclass(frozen=True)
class ConfigurationBounds:
    """Inclusive lower and upper limits for configurations of one dimension."""

    lower: Configuration
    upper: Configuration

    def __post_init__(self) -> None:
        # TODO 3: validate types, dimensions, and lower < upper in every coordinate.
        raise NotImplementedError("TODO 3: validate ConfigurationBounds")

    @property
    def dimension(self) -> int:
        """Return the configuration dimension accepted by these bounds."""
        # TODO 3: return the validated common dimension.
        raise NotImplementedError("TODO 3: implement ConfigurationBounds.dimension")

    def contains(self, configuration: Configuration) -> bool:
        """Return whether a configuration lies inside the inclusive bounds."""
        # TODO 4: reject an incompatible object and test inclusive limits.
        raise NotImplementedError("TODO 4: implement ConfigurationBounds.contains")


@dataclass(frozen=True)
class Path:
    """An ordered sequence of compatible configurations."""

    waypoints: Sequence[Configuration]

    def __post_init__(self) -> None:
        # TODO 5: own a tuple and validate count, type, and dimension.
        raise NotImplementedError("TODO 5: validate Path")

    @property
    def dimension(self) -> int:
        """Return the common waypoint dimension."""
        # TODO 5
        raise NotImplementedError("TODO 5: implement Path.dimension")

    @property
    def start(self) -> Configuration:
        """Return the first waypoint."""
        # TODO 5
        raise NotImplementedError("TODO 5: implement Path.start")

    @property
    def goal(self) -> Configuration:
        """Return the last waypoint."""
        # TODO 5
        raise NotImplementedError("TODO 5: implement Path.goal")

    def as_array(self) -> NDArray[np.float64]:
        """Return an owned array with shape ``(N, D)``."""
        # TODO 5
        raise NotImplementedError("TODO 5: implement Path.as_array")

    def length(self) -> float:
        """Return Euclidean polyline length via the supplied pure function."""
        # TODO 5: delegate the numerical calculation to polyline_length.
        raise NotImplementedError("TODO 5: implement Path.length")


@dataclass(frozen=True)
class PlanningProblem:
    """Start, goal, and valid bounds for one planning request."""

    problem_id: str
    start: Configuration
    goal: Configuration
    bounds: ConfigurationBounds

    def __post_init__(self) -> None:
        # TODO 6: validate the ID, composed object types, dimensions, and bounds.
        raise NotImplementedError("TODO 6: validate PlanningProblem")


@dataclass(frozen=True)
class PlanResult:
    """A successful path or an explained failure for one planning problem."""

    problem: PlanningProblem
    path: Path | None
    message: str = ""

    def __post_init__(self) -> None:
        # TODO 7: enforce the success/failure and path/problem invariants.
        raise NotImplementedError("TODO 7: validate PlanResult")

    @property
    def succeeded(self) -> bool:
        """Return True exactly when this result contains a path."""
        # TODO 7
        raise NotImplementedError("TODO 7: implement PlanResult.succeeded")

