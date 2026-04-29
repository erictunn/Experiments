"""Graphing experiments for different maths concepts.
Engineered to be easy to add more graphs."""


from typing import List

import numpy as np

from grapher import Grapher, ImagePlotData, LinePlotData, PlotData


class MathGraph:
    """Base class for a graphable maths concept."""

    def __init__(self, grapher: Grapher | None = None):
        self.grapher = grapher or Grapher()

    def generate_data(self) -> PlotData:
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

    def generate_data(self) -> LinePlotData:
        base_multiplier = int(input("Enter a base multiplier for i: "))
        n = int(input("Enter a number of tetration steps: "))
        base = base_multiplier * 1j

        points = self.i_tetration_maths(base, n)
        real = [point.real for point in points]
        imaginary = [point.imag for point in points]

        return LinePlotData(
            x_1=real,
            y_1=imaginary,
            title=f"Tetration Path for {base} ({n} steps)",
            x_label="Real Part",
            y_label="Imaginary Part",
        )


class SinhGraph(MathGraph):
    """Graph of the hyperbolic sine function."""

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


class MandelbrotGraph(MathGraph):
    """Graph of the Mandelbrot set."""

    COLOUR_MAPS = {
        "1": "twilight_shifted",
        "2": "inferno",
        "3": "magma",
        "4": "viridis",
        "5": "plasma",
        "6": "turbo",
    }

    def generate_data(self) -> ImagePlotData:
        max_iterations = int(input("Enter the maximum number of iterations for the Mandelbrot set: "))
        x_res = int(input("Enter the resolution for the x axis (e.g. 1920): "))
        y_res = int(input("Enter the resolution for the y axis (e.g. 1080): "))
        cmap_choice = input(
            "Choose a colour scheme:"
            "\n1: twilight_shifted"
            "\n2: inferno"
            "\n3: magma"
            "\n4: viridis"
            "\n5: plasma"
            "\n6: turbo"
            "\nPress Enter for default (twilight_shifted): "
        ).strip()
        save_path = input("Optional PNG output path (leave blank to skip saving): ").strip() or None
        cmap = self.COLOUR_MAPS.get(cmap_choice, "twilight_shifted")

        x_centre = -0.5
        y_centre = 0.0
        y_span = 3.0
        aspect_ratio = x_res / y_res
        x_span = y_span * aspect_ratio
        x_min = x_centre - x_span / 2
        x_max = x_centre + x_span / 2
        y_min = y_centre - y_span / 2
        y_max = y_centre + y_span / 2
        x = np.linspace(x_min, x_max, x_res)
        y = np.linspace(y_min, y_max, y_res)
        c = x[None, :] + 1j * y[:, None]
        z = np.zeros_like(c)
        output = np.zeros(c.shape, dtype=int)

        for iteration in range(max_iterations):
            mask = np.abs(z) < 2
            output[mask] = iteration
            z[mask] = z[mask] ** 2 + c[mask]

        return ImagePlotData(
            image=output,
            title=f"Mandelbrot Set ({max_iterations} iterations)",
            x_label="Real Axis",
            y_label="Imaginary Axis",
            axis="off" if save_path else "auto",
            extent=(x_min, x_max, y_min, y_max),
            cmap=cmap,
            interpolation="nearest",
            save_path=save_path,
            save_dpi=300,
            export_clean=bool(save_path),
        )


if __name__ == "__main__":
    graph_options = {
        1: ImaginaryTetrationGraph,
        2: SinhGraph,
        3: MandelbrotGraph,
    }
    # TODO: Make menu self document from the options table.
    choice = int(
        input(
            "Enter a number for what concept you want a graph of. "
            "\n1: imaginary unit tetration. "
            "\n2: hyperbolic sine function. "
            "\n3: Mandelbrot set. \nYour choice: "
        )
    )
    graph_class = graph_options.get(choice)
    if graph_class is None:
        raise ValueError(f"Unknown graph choice: {choice}")
    graph_class().run()
