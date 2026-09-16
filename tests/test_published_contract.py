"""Published contract tests for Week 3 planning-domain objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, is_dataclass

import numpy as np
import pytest

from ap_week03_planning import (
    Configuration,
    ConfigurationBounds,
    Path,
    PlanResult,
    PlanningModelError,
    PlanningProblem,
    PlanningRun,
)


def bounds_2d() -> ConfigurationBounds:
    return ConfigurationBounds(Configuration((0.0, 0.0)), Configuration((4.0, 3.0)))


def problem_2d(problem_id: str = "p-demo") -> PlanningProblem:
    return PlanningProblem(
        problem_id,
        Configuration((0.0, 0.0)),
        Configuration((3.2, 2.0)),
        bounds_2d(),
    )


def valid_path(problem: PlanningProblem | None = None) -> Path:
    active = problem or problem_2d()
    return Path(
        (
            active.start,
            Configuration((1.0, 1.4)),
            Configuration((2.4, 1.1)),
            active.goal,
        )
    )


def test_public_error_is_a_value_error() -> None:
    assert issubclass(PlanningModelError, ValueError)


@pytest.mark.parametrize(
    "object_type",
    [Configuration, ConfigurationBounds, Path, PlanningProblem, PlanResult, PlanningRun],
)
def test_public_object_is_a_dataclass(object_type: type[object]) -> None:
    assert is_dataclass(object_type)


@pytest.mark.parametrize(
    "factory,field_name,new_value",
    [
        (lambda: Configuration((1.0, 2.0)), "values", (9.0, 9.0)),
        (lambda: bounds_2d(), "lower", Configuration),
        (lambda: valid_path(), "waypoints", ()),
        (lambda: problem_2d(), "problem_id", "changed"),
        (lambda: PlanResult(problem_2d(), valid_path(), "ok"), "message", "changed"),
    ],
)
def test_value_objects_reject_field_reassignment(
    factory: object, field_name: str, new_value: object
) -> None:
    instance = factory()  # type: ignore[operator]
    with pytest.raises(FrozenInstanceError):
        setattr(instance, field_name, new_value)


@pytest.mark.parametrize(
    "source,expected",
    [
        ((1, 2), (1.0, 2.0)),
        ([1.5, -2.25], (1.5, -2.25)),
        (np.array([0, 3], dtype=np.int64), (0.0, 3.0)),
        (np.array([0.25, 0.5], dtype=np.float32), (0.25, 0.5)),
    ],
)
def test_configuration_normalizes_an_owned_float_tuple(source: object, expected: tuple[float, ...]) -> None:
    configuration = Configuration(source)  # type: ignore[arg-type]
    assert configuration.values == expected
    assert isinstance(configuration.values, tuple)


@pytest.mark.parametrize("values", [(1.0,), (1.0, 2.0), (1.0, 2.0, 3.0, 4.0)])
def test_configuration_reports_dimension(values: tuple[float, ...]) -> None:
    assert Configuration(values).dimension == len(values)


@pytest.mark.parametrize(
    "invalid",
    [
        (),
        [],
        "12",
        [[1.0, 2.0]],
        [True, False],
        np.array([True, False]),
        [1.0 + 2.0j, 2.0 + 0.0j],
        ["1.0", "2.0"],
        np.array([1.0, "2.0"], dtype=object),
        [np.nan, 1.0],
        [np.inf, 1.0],
    ],
)
def test_configuration_rejects_invalid_values(invalid: object) -> None:
    with pytest.raises(PlanningModelError):
        Configuration(invalid)  # type: ignore[arg-type]


def test_configuration_breaks_alias_with_input_array() -> None:
    source = np.array([1.0, 2.0])
    configuration = Configuration(source)
    source[0] = 99.0
    assert configuration.values == (1.0, 2.0)


def test_configuration_as_array_returns_float64_copy() -> None:
    configuration = Configuration((1.0, 2.0))
    first = configuration.as_array()
    second = configuration.as_array()
    first[0] = 99.0
    assert first.dtype == np.float64
    assert np.array_equal(second, np.array([1.0, 2.0]))
    assert configuration.values == (1.0, 2.0)


def test_dataclass_equality_compares_configuration_values() -> None:
    assert Configuration((1, 2)) == Configuration((1.0, 2.0))


def test_configuration_repr_names_the_field() -> None:
    assert "values=" in repr(Configuration((1.0, 2.0)))


def test_bounds_dimension_is_shared_dimension() -> None:
    assert bounds_2d().dimension == 2


@pytest.mark.parametrize(
    "point,expected",
    [
        ((0.0, 0.0), True),
        ((4.0, 3.0), True),
        ((2.0, 1.5), True),
        ((-0.001, 1.0), False),
        ((2.0, 3.001), False),
    ],
)
def test_bounds_contains_uses_inclusive_limits(point: tuple[float, float], expected: bool) -> None:
    assert bounds_2d().contains(Configuration(point)) is expected


@pytest.mark.parametrize(
    "lower,upper",
    [
        ((0.0, 0.0), (1.0,)),
        ((0.0, 0.0), (0.0, 1.0)),
        ((1.0, 0.0), (0.0, 1.0)),
    ],
)
def test_bounds_reject_invalid_limit_relationships(
    lower: tuple[float, ...], upper: tuple[float, ...]
) -> None:
    with pytest.raises(PlanningModelError):
        ConfigurationBounds(Configuration(lower), Configuration(upper))


def test_bounds_require_configuration_objects() -> None:
    with pytest.raises(PlanningModelError):
        ConfigurationBounds((0.0, 0.0), Configuration((1.0, 1.0)))  # type: ignore[arg-type]


def test_bounds_contains_rejects_wrong_dimension() -> None:
    with pytest.raises(PlanningModelError):
        bounds_2d().contains(Configuration((1.0, 2.0, 3.0)))


def test_path_owns_a_tuple_of_waypoints() -> None:
    source = [Configuration((0.0, 0.0)), Configuration((1.0, 1.0))]
    path = Path(source)
    source.append(Configuration((2.0, 2.0)))
    assert isinstance(path.waypoints, tuple)
    assert len(path.waypoints) == 2


def test_path_reports_start_goal_and_dimension() -> None:
    path = valid_path()
    assert path.start == Configuration((0.0, 0.0))
    assert path.goal == Configuration((3.2, 2.0))
    assert path.dimension == 2


def test_path_as_array_has_n_by_d_shape_and_is_owned() -> None:
    path = valid_path()
    first = path.as_array()
    second = path.as_array()
    first[0, 0] = 100.0
    assert first.shape == (4, 2)
    assert first.dtype == np.float64
    assert second[0, 0] == pytest.approx(0.0)


def test_path_length_delegates_to_euclidean_polyline_calculation() -> None:
    path = Path((Configuration((0.0, 0.0)), Configuration((3.0, 0.0)), Configuration((3.0, 4.0))))
    assert path.length() == pytest.approx(7.0)


@pytest.mark.parametrize("case", ["empty", "single", "wrong-type", "mixed-dimension"])
def test_path_rejects_invalid_waypoint_sequence(case: str) -> None:
    waypoints: object
    if case == "empty":
        waypoints = ()
    elif case == "single":
        waypoints = (Configuration((0.0, 0.0)),)
    elif case == "wrong-type":
        waypoints = (Configuration((0.0, 0.0)), (1.0, 1.0))
    else:
        waypoints = (Configuration((0.0, 0.0)), Configuration((1.0, 1.0, 1.0)))
    with pytest.raises(PlanningModelError):
        Path(waypoints)  # type: ignore[arg-type]


@pytest.mark.parametrize("problem_id", ["", "   ", 7, None])
def test_problem_rejects_invalid_id(problem_id: object) -> None:
    with pytest.raises(PlanningModelError):
        PlanningProblem(problem_id, Configuration((0.0, 0.0)), Configuration((1.0, 1.0)), bounds_2d())  # type: ignore[arg-type]


def test_problem_normalizes_surrounding_id_whitespace() -> None:
    assert problem_2d("  p-17  ").problem_id == "p-17"


@pytest.mark.parametrize(
    "start,goal",
    [
        ((0.0,), (1.0, 1.0)),
        ((-1.0, 0.0), (1.0, 1.0)),
        ((0.0, 0.0), (5.0, 1.0)),
    ],
)
def test_problem_rejects_incompatible_or_out_of_bounds_endpoints(
    start: tuple[float, ...], goal: tuple[float, ...]
) -> None:
    with pytest.raises(PlanningModelError):
        PlanningProblem("p", Configuration(start), Configuration(goal), bounds_2d())


def test_problem_requires_composed_domain_objects() -> None:
    with pytest.raises(PlanningModelError):
        PlanningProblem("p", (0.0, 0.0), Configuration((1.0, 1.0)), bounds_2d())  # type: ignore[arg-type]


def test_success_result_reports_succeeded() -> None:
    problem = problem_2d()
    result = PlanResult(problem, valid_path(problem), "valid candidate")
    assert result.succeeded is True


def test_failure_result_reports_not_succeeded_and_normalizes_message() -> None:
    result = PlanResult(problem_2d(), None, "  no path within budget  ")
    assert result.succeeded is False
    assert result.message == "no path within budget"


@pytest.mark.parametrize("message", ["", "   "])
def test_failed_result_requires_explanation(message: str) -> None:
    with pytest.raises(PlanningModelError):
        PlanResult(problem_2d(), None, message)


def test_result_rejects_wrong_path_endpoint() -> None:
    problem = problem_2d()
    wrong = Path((problem.start, Configuration((2.0, 1.0))))
    with pytest.raises(PlanningModelError):
        PlanResult(problem, wrong, "wrong endpoint")


def test_result_rejects_out_of_bounds_intermediate_waypoint() -> None:
    problem = problem_2d()
    wrong = Path((problem.start, Configuration((5.0, 1.0)), problem.goal))
    with pytest.raises(PlanningModelError):
        PlanResult(problem, wrong, "outside bounds")


def test_result_rejects_non_string_message() -> None:
    problem = problem_2d()
    with pytest.raises(PlanningModelError):
        PlanResult(problem, valid_path(problem), 7)  # type: ignore[arg-type]


def test_planning_run_starts_empty() -> None:
    run = PlanningRun(problem_2d())
    assert run.results == ()
    assert run.latest is None


def test_planning_run_records_compatible_results_in_order() -> None:
    problem = problem_2d()
    first = PlanResult(problem, None, "first attempt failed")
    second = PlanResult(problem, valid_path(problem), "second attempt succeeded")
    run = PlanningRun(problem)
    run.record_result(first)
    run.record_result(second)
    assert run.results == (first, second)
    assert run.latest is second


def test_planning_runs_do_not_share_default_history() -> None:
    problem = problem_2d()
    first = PlanningRun(problem)
    second = PlanningRun(problem)
    first.record_result(PlanResult(problem, None, "failed"))
    assert len(first.results) == 1
    assert second.results == ()


def test_results_property_does_not_expose_mutable_internal_list() -> None:
    problem = problem_2d()
    run = PlanningRun(problem)
    snapshot = run.results
    assert isinstance(snapshot, tuple)
    assert snapshot == ()


def test_run_rejects_result_for_different_problem_without_mutating_history() -> None:
    run = PlanningRun(problem_2d("p-one"))
    other = problem_2d("p-two")
    with pytest.raises(PlanningModelError):
        run.record_result(PlanResult(other, None, "different problem"))
    assert run.results == ()


def test_run_rejects_non_result_without_mutating_history() -> None:
    run = PlanningRun(problem_2d())
    with pytest.raises(PlanningModelError):
        run.record_result("not a result")  # type: ignore[arg-type]
    assert run.results == ()


def test_run_uses_default_factory_for_hidden_results_field() -> None:
    result_field = next(item for item in fields(PlanningRun) if item.name == "_results")
    assert result_field.default_factory is list
    assert result_field.init is False
    assert result_field.repr is False
