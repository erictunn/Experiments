"""Build the Mandelbrot C++ extension."""

from pathlib import Path

import numpy
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

setup(
    name="graphs_maths",
    ext_modules=[
        Extension(
            "mandel_lib",
            [str(Path(__file__).with_name("mandelbrot_maths.cpp"))],
            include_dirs=[numpy.get_include()],
            language="c++",
            extra_compile_args=["-O3", "-std=c++17"],
        ),
        Extension(
            "julia_lib",
            [str(Path(__file__).with_name("julia_set_maths.cpp"))],
            include_dirs=[numpy.get_include()],
            language="c++",
            extra_compile_args=["-O3", "-std=c++17"],
        ),
    ],
    cmdclass={"build_ext": build_ext},
)
