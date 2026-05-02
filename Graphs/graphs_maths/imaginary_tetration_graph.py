"""Graph of the tetration of (x*i) to n steps."""

import numpy as np
from numba import jit

from grapher import LinePlotData
from graphs_maths.math_graph import MathGraph


class ImaginaryTetrationGraph(MathGraph):
    @staticmethod
    @jit(nopython=True)
    def _i_tetration_maths(base: complex, n: int) -> np.ndarray:
        results = np.empty(n, dtype=np.complex128)
        if n <= 0:
            return results

        results[0] = base
        for i in range(1, n):
            results[i] = base ** results[i - 1]
        return results

    def generate_data(self) -> LinePlotData:
        base_multiplier = int(input("Enter a base multiplier for i: "))
        n = int(input("Enter a number of tetration steps: "))
        base = base_multiplier * 1j

        points = self._i_tetration_maths(base, n)
        real = [point.real for point in points]
        imaginary = [point.imag for point in points]

        return LinePlotData(
            x_1=real,
            y_1=imaginary,
            title=f"Tetration Path for {base} ({n} steps)",
            x_label="Real Part",
            y_label="Imaginary Part",
        )
