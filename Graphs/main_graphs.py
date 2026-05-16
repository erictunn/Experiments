"""Graphing experiments for different maths concepts.
This is the main file from which this project can be run.
For the mandelbrot/julia sets to work,
you must run the commands listed in setup.py to build the C++ extensions."""

from graphs_maths.imaginary_tetration_graph import ImaginaryTetrationGraph
from graphs_maths.julia_graph import JuliaGraph
from graphs_maths.mandelbrot_graph import MandelbrotGraph
from graphs_maths.sinh_graph import SinhGraph


if __name__ == "__main__":
    graph_options = {
        1: ImaginaryTetrationGraph,
        2: SinhGraph,
        3: MandelbrotGraph,
        4: JuliaGraph,
    }
    input_dialogue = "Enter a number for what concept you want a graph of. "\
            "\n1: imaginary unit tetration. "\
            "\n2: hyperbolic sine function. "\
            "\n3: Mandelbrot set. "\
            "\n4: Julia set. \nYour choice: "
    # TODO: make dialogue self document from graph options.
    choice = int(
        input(
            input_dialogue
        )
    )
    graph_class = graph_options.get(choice)
    if graph_class is None:
        raise ValueError(f"Unknown graph choice: {choice}")
    graph_class().run()
