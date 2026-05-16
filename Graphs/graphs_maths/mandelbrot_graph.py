"""Graph of the Mandelbrot set."""

from grapher import ImagePlotData
from graphs_maths.math_graph import MathGraph
from .input_helper import get_cmap

from . import mandel_lib


class MandelbrotGraph(MathGraph):


    def generate_data(self) -> ImagePlotData:
        max_iterations = int(input("Enter the maximum number of iterations for the Mandelbrot set: "))
        x_res = int(input("Enter the resolution for the x axis (e.g. 1920): "))
        y_res = int(input("Enter the resolution for the y axis (e.g. 1080): "))

        cmap = get_cmap() if not None else "twilight_shifted"

        save_path = input("Optional PNG output path (leave blank to skip saving): ").strip() or None

        x_centre = -0.5
        y_centre = 0.0
        y_span = 3.0
        aspect_ratio = x_res / y_res
        x_span = y_span * aspect_ratio
        x_min = x_centre - x_span / 2
        x_max = x_centre + x_span / 2
        y_min = y_centre - y_span / 2
        y_max = y_centre + y_span / 2

        output = mandel_lib.generate(x_min, x_max, y_min, y_max, x_res, y_res, max_iterations)

        return ImagePlotData(
            image=output,
            title=f"Mandelbrot Set ({max_iterations} iterations)",
            x_label="Real Axis",
            y_label="Imaginary Axis",
            axis="off" if save_path else "auto",
            extent=(x_min, x_max, y_min, y_max),
            cmap=cmap,
            interpolation="bilinear",
            save_path=save_path,
            save_dpi=300,
            export_clean=bool(save_path),
        )
