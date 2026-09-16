"""Protected SVG caller for the deterministic Week 3 example."""

from __future__ import annotations

from html import escape

from .history import PlanningRun


def planning_run_svg(run: PlanningRun) -> str:
    """Return a simple SVG view of the latest two-dimensional successful path."""
    result = run.latest
    if result is None or not result.succeeded or result.path is None:
        raise ValueError("the preview requires a recorded successful path")
    points = result.path.as_array()
    if points.shape[1] != 2:
        raise ValueError("the preview supports only two-dimensional configurations")

    width, height, padding = 760.0, 430.0, 60.0
    lower = run.problem.bounds.lower.as_array()
    upper = run.problem.bounds.upper.as_array()
    scale_x = (width - 2.0 * padding) / (upper[0] - lower[0])
    scale_y = (height - 2.0 * padding) / (upper[1] - lower[1])

    def screen(point: object) -> tuple[float, float]:
        x, y = point  # type: ignore[misc]
        return padding + (x - lower[0]) * scale_x, height - padding - (y - lower[1]) * scale_y

    screen_points = [screen(point) for point in points]
    polyline = " ".join(f"{x:.2f},{y:.2f}" for x, y in screen_points)
    circles = []
    labels = []
    for index, (x, y) in enumerate(screen_points):
        circles.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7" fill="white" stroke="black" stroke-width="2"/>')
        label = "start" if index == 0 else "goal" if index == len(screen_points) - 1 else f"q{index}"
        # Keep an interior label below a segment that rises to its right.
        # In the supplied example this clears q2 without changing the path.
        rises_right = (
            0 < index < len(screen_points) - 1
            and screen_points[index + 1][0] > x
            and screen_points[index + 1][1] < y
        )
        label_x = x - 38.0 if index == 0 else x + 10.0
        label_y = y - 14.0 if index == 0 else y + 28.0 if rises_right else y - 10.0
        labels.append(f'<text x="{label_x:.2f}" y="{label_y:.2f}" font-family="serif" font-size="18">{escape(label)}</text>')

    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="430" viewBox="0 0 760 430">',
            '<rect width="760" height="430" fill="white"/>',
            '<rect x="60" y="60" width="640" height="310" fill="#f6f6f6" stroke="black" stroke-width="2"/>',
            f'<text x="60" y="35" font-family="serif" font-size="22">Problem: {escape(run.problem.problem_id)}</text>',
            f'<polyline points="{polyline}" fill="none" stroke="#333333" stroke-width="5"/>',
            *circles,
            *labels,
            '<text x="60" y="410" font-family="serif" font-size="16">Display of supplied path objects; not a planner or physics simulation.</text>',
            "</svg>",
        ]
    )
