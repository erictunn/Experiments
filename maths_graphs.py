"""Graphing experiments for different maths concepts.
Engineered to be easy to add more graphs."""

from dataclasses import dataclass, field
from typing import List
import numpy as np

import matplotlib.pyplot as plt


@dataclass
class GraphData:
    x_1: List[float] = field(default_factory=list)
    y_1: List[float] = field(default_factory=list)
    x_2: List[float] = field(default_factory=list)
    y_2: List[float] = field(default_factory=list)
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    line_label: str = ""
    axis: str = "equal"
    xscale: str = "linear"
    yscale: str = "linear"


class Grapher:
    def graph(self, data: GraphData) -> None:

        plt.figure()
        plt.plot(data.x_1, data.y_1, label=data.line_label or None)

        plt.axhline(0, color="black", linewidth=0.5)
        plt.axvline(0, color="black", linewidth=0.5)
        plt.grid(True)
        plt.title(data.title)
        plt.xlabel(data.x_label)
        plt.ylabel(data.y_label)
        if data.line_label:
            plt.legend()
        plt.xscale(data.xscale)
        plt.yscale(data.yscale)
        plt.axis(data.axis)
        plt.show()


class MathGraph:
    """Base class for a graphable maths concept."""

    def __init__(self, grapher: Grapher | None = None):
        self.grapher = grapher or Grapher()

    def generate_data(self) -> GraphData:
        """Subclasses must implement this method to generate the data for the graph."""
        raise NotImplementedError("Subclasses must implement generate_data().")

    def run(self) -> None:
        """Generates the data and graphs it."""
        data = self.generate_data()
        self.grapher.graph(data)


class ImaginaryTetrationGraph(MathGraph):
    """Graph of the tetration of (x*i) to n steps."""
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
            x_1=real,
            y_1=imaginary,
            title=f"Tetration Path for {base} ({n} steps)",
            x_label="Real Part",
            y_label="Imaginary Part",
        )

class SinhGraph(MathGraph):
    """Graph of the hyperbolic sine function."""

    def generate_data(self) -> GraphData:
        start_n = int(input("Enter a start for the graph on the x axis: "))
        end_n = int(input("Enter an end for the graph on the x axis: "))
        use_symlog = input(
            "Would you like the graph to use symlog for the yscale? "
            "\nEnter True for symlog or False for linear: "
        ).strip().lower() in {"true", "t", "yes", "y", "1"}
        yscale = "symlog" if use_symlog else "linear"
        x = np.linspace(start_n, end_n, 1000)
        y = np.sinh(x)
        return GraphData(
            x_1=x.tolist(),
            y_1=y.tolist(),
            title="Hyperbolic Sine Function",
            x_label="x",
            y_label="sinh(x)",
            line_label="sinh(x)",
            axis="auto",
            xscale="linear",
            yscale=yscale,
        )


if __name__ == "__main__":
    graph_options = {
        1: ImaginaryTetrationGraph,
        2: SinhGraph,
    }
    # TODO: Make menu self document from the options table.
    choice = int(
        input(
            "Enter a number for what concept you want a graph of. "
            "\n1: imaginary unit tetration. "
            "\n2: hyperbolic sine function. \n"
        )
    )
    graph_class = graph_options.get(choice)
    if graph_class is None:
        raise ValueError(f"Unknown graph choice: {choice}")
    graph_class().run()
