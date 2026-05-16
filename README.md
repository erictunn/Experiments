# Experiments

A collection of mini projects and one-off ideas I've coded while learning and experimenting.
Anything not big enough to deserve its own repo, but represents a meaningful step in my development as a programmer, goes here.

## What's in here

**Graphs** – Mathematical visualisations I've made to assist understanding of interesting concepts I found difficult. The most notable examples are Mandelbrot/Julia set renderers,
for which I wrote extensions in C++, and a visualisation of tetration of the imaginary unit.

**Other experiments** – Various experiments with new libraries and ideas. These are currently only Python.

## Running

Individual files not part of a folder can be just run. When there is a folder (Graphs), look for the file of which the name starts with main. There will be further instructions there.

## Why C++ in a Python project?

I have written C++ extensions as a way to explore optimisation.
My original Python implementation for generating Mandelbrot sets was extremely slow, and a NumPy-based approach using boolean masks consumed too much memory.
As such, I switched to for loops with multithreading in C++.
