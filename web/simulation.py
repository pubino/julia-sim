"""The original JuliaCanvas recurrence, including its adaptive threshold."""

import json
from math import isfinite, sqrt
from typing import cast

import numpy as np

SIZE = 300
INITIAL_THRESHOLD = 1000.0
UPDATE_LIMIT = 1e100


class Simulation:
    def __init__(self, left: float, right: float, bottom: float, top: float) -> None:
        i = np.arange(SIZE, dtype=np.float64)
        self.x = (left + i * (right - left) / SIZE)[:, None]
        self.y = (bottom + i * (top - bottom) / SIZE)[None, :]
        self.real = np.zeros((SIZE, SIZE), dtype=np.float64)
        self.imag = np.zeros_like(self.real)
        self.dark = np.zeros((SIZE, SIZE), dtype=np.bool_)
        self.steps = 0
        self.threshold = INITIAL_THRESHOLD

    def advance(self, steps: int) -> None:
        if type(steps) is not int or not 1 <= steps <= 16:
            raise ValueError("Use 1 to 16 iterations per update.")
        for _ in range(steps):
            real = self.real * self.real - self.imag * self.imag + self.x
            imag = 2 * self.real * self.imag + self.y
            norm_squared = real * real + imag * imag
            keep = norm_squared < UPDATE_LIMIT
            self.dark[:] = norm_squared > self.threshold
            np.copyto(self.real, real, where=keep)
            np.copyto(self.imag, imag, where=keep)
            self.threshold = sqrt(float(norm_squared.max()))
            self.steps += 1

    def frame(self) -> tuple[int, int, float, bytes]:
        return (
            self.steps,
            int(np.count_nonzero(self.dark)),
            self.threshold,
            self.dark[:, ::-1].T.tobytes(),
        )


def create(parameters: str) -> Simulation:
    values = json.loads(parameters, parse_int=float)
    if (
        not isinstance(values, list)
        or len(values) != 4
        or not all(type(value) is float and isfinite(value) for value in values)
    ):
        raise ValueError("Enter four finite viewport bounds.")
    left, right, bottom, top = cast(list[float], values)
    if not (-1000 <= left < right <= 1000 and -1000 <= bottom < top <= 1000):
        raise ValueError(
            "Use increasing real and imaginary bounds between −1,000 and 1,000."
        )
    if min(right - left, top - bottom) < 1e-12:
        raise ValueError("Use spans of at least 0.000000000001 on both axes.")
    return Simulation(left, right, bottom, top)
