"""Graph of the Julia set."""

from grapher import ImagePlotData
from graphs_maths.math_graph import MathGraph
from . import julia_lib


class JuliaGraph(MathGraph):
    """Starter implementation for plotting Julia sets."""

    COLOUR_MAPS = {
        "1": "twilight_shifted",
        "2": "inferno",
        "3": "magma",
        "4": "flag",
        "5": "plasma",
        "6": "turbo",
        "7": "spectral",
        "8": "cividis",
        "9": "cubehelix",
        "10": "cool",
    }


    def generate_data(self) -> ImagePlotData:
        max_iterations = int(input("Enter the maximum number of iterations for the Julia set: "))
        x_res = int(input("Enter the resolution for the x axis (e.g. 1920): "))
        y_res = int(input("Enter the resolution for the y axis (e.g. 1080): "))
        c_real = float(input("Enter the real part for the Julia constant c (e.g. -0.8): "))
        c_imag = float(input("Enter the imaginary part for the Julia constant c (e.g. 0.156): "))

        cmap_choice = input(
            "Choose a colour scheme:"
            "\n1: twilight_shifted"
            "\n2: inferno"
            "\n3: magma"
            "\n4: flag"
            "\n5: plasma"
            "\n6: turbo"
            "\n7: spectral"
            "\n8: cividis"
            "\n9: cubehelix"
            "\n10: cool"
            "\nPress Enter for default (twilight_shifted): "
        ).strip()

        save_path = input("Optional PNG output path (leave blank to skip saving): ").strip() or None
        cmap = self.COLOUR_MAPS.get(cmap_choice, "twilight_shifted")

        x_centre = 0.0
        y_centre = 0.0
        y_span = 3.0
        aspect_ratio = x_res / y_res
        x_span = y_span * aspect_ratio
        x_min = x_centre - x_span / 2
        x_max = x_centre + x_span / 2
        y_min = y_centre - y_span / 2
        y_max = y_centre + y_span / 2

        output = julia_lib.generate(
            x_min, x_max, y_min, y_max, x_res, y_res, max_iterations, c_real, c_imag
        )

        return ImagePlotData(
            image=output,
            title=f"Julia Set c={c_real}+{c_imag}i ({max_iterations} iterations)",
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
