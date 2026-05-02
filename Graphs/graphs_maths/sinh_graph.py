"""Graph of the hyperbolic sine function."""

import numpy as np

from grapher import LinePlotData
from graphs_maths.math_graph import MathGraph


class SinhGraph(MathGraph):
    def generate_data(self) -> LinePlotData:
        start_n = int(input("Enter a start for the graph on the x axis: "))
        end_n = int(input("Enter an end for the graph on the x axis: "))
        use_symlog = input(
            "Would you like the graph to use symlog for the yscale? "
            "\nEnter True for symlog or False for linear: "
        ).strip().lower() in {"true", "t", "yes", "y", "1"}
        yscale = "symlog" if use_symlog else "linear"
        x = np.linspace(start_n, end_n, 1000)
        y = np.sinh(x)
        return LinePlotData(
            x_1=x,
            y_1=y,
            title="Hyperbolic Sine Function",
            x_label="x",
            y_label="sinh(x)",
            line_label="sinh(x)",
            axis="auto",
            xscale="linear",
            yscale=yscale,
        )
