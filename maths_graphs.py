"""Graphing experiments for different maths concepts.
Engineered to be easy to add more graphs."""

from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt


@dataclass
class GraphData:
    x: List[float] = field(default_factory=list)
    y: List[float] = field(default_factory=list)
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    line_label: str = ""


class Grapher:
    def graph(self, data: GraphData) -> None:
        plt.figure()
        plt.plot(data.x, data.y, label=data.line_label or None)

        plt.axhline(0, color="black", linewidth=0.5)
        plt.axvline(0, color="black", linewidth=0.5)
        plt.grid(True)
        plt.title(data.title)
        plt.xlabel(data.x_label)
        plt.ylabel(data.y_label)
        if data.line_label:
            plt.legend()
        plt.axis("equal")
        plt.show()


class MathGraph:
    """Base class for a graphable maths concept."""

    def __init__(self, grapher: Grapher | None = None):
        self.grapher = grapher or Grapher()

    def generate_data(self) -> GraphData:
        raise NotImplementedError("Subclasses must implement generate_data().")

    def run(self) -> None:
        data = self.generate_data()
        self.grapher.graph(data)


class ImaginaryTetrationGraph(MathGraph):
    @staticmethod
    def i_tetration_maths(base: complex, n: int) -> List[complex]:
        """For n steps: i, i^i, i^(i^i), ..."""
        if n <= 0:
            return []

        results = [base]
        for _ in range(n - 1):
            results.append(base ** results[-1])
        return results

    def generate_data(self) -> GraphData:
        base_multiplier = int(input("Enter a base multiplier for i: "))
        n = int(input("Enter a number of tetration steps: "))
        base = base_multiplier * 1j

        points = self.i_tetration_maths(base, n)
        real = [point.real for point in points]
        imaginary = [point.imag for point in points]

        return GraphData(
            x=real,
            y=imaginary,
            title=f"Tetration Path for {base} ({n} steps)",
            x_label="Real Part",
            y_label="Imaginary Part",
        )


if __name__ == "__main__":
    choice = int(input("Enter a number for what concept you want a graph of. " \
    "\n1: imaginary unit tetration. "))
    if choice == 1: # TODO - use dict or similar rather than if-elif-...
        ImaginaryTetrationGraph().run()
