"""Supplied pure numerical functions reused by the Week 3 objects."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def polyline_length(points: NDArray[np.float64]) -> float:
    """Return the Euclidean length of a validated ``(N, D)`` point array."""
    array = np.asarray(points, dtype=np.float64)
    if array.ndim != 2 or array.shape[0] < 2 or array.shape[1] < 1:
        raise ValueError("points must have shape (N, D) with N >= 2 and D >= 1")
    if not np.isfinite(array).all():
        raise ValueError("points must contain finite values")
    return float(np.linalg.norm(np.diff(array, axis=0), axis=1).sum())

