"""Base graph class for maths concepts."""

from grapher import Grapher, PlotData


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
