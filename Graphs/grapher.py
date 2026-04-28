from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeAlias

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class BasePlotData:
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    axis: str = "equal"
    xscale: str = "linear"
    yscale: str = "linear"
    save_path: str | None = None
    save_dpi: int = 300


@dataclass
class LinePlotData(BasePlotData):
    x_1: list[float] | np.ndarray = field(default_factory=list)
    y_1: list[float] | np.ndarray = field(default_factory=list)
    x_2: list[float] | np.ndarray = field(default_factory=list)
    y_2: list[float] | np.ndarray = field(default_factory=list)
    line_label: str = ""


@dataclass
class ImagePlotData(BasePlotData):
    image: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    extent: tuple[float, float, float, float] | None = None
    cmap: str = "magma"
    interpolation: str = "nearest"
    origin: str = "lower"
    show_colorbar: bool = False


PlotData: TypeAlias = LinePlotData | ImagePlotData


class Grapher:
    def graph(self, data: PlotData) -> None:
        if isinstance(data, LinePlotData):
            self._graph_line(data)
            return
        if isinstance(data, ImagePlotData):
            self._graph_image(data)
            return
        raise TypeError(f"Unsupported plot data type: {type(data).__name__}")

    def _graph_line(self, data: LinePlotData) -> None:
        fig, ax = plt.subplots()
        ax.plot(data.x_1, data.y_1, label=data.line_label or None)

        if len(data.x_2) and len(data.y_2):
            ax.plot(data.x_2, data.y_2)

        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.grid(True)
        ax.set_title(data.title)
        ax.set_xlabel(data.x_label)
        ax.set_ylabel(data.y_label)
        if data.line_label:
            ax.legend()
        ax.set_xscale(data.xscale)
        ax.set_yscale(data.yscale)
        ax.axis(data.axis)

        self._save_if_requested(fig, data)
        plt.show()

    def _graph_image(self, data: ImagePlotData) -> None:
        fig, ax = plt.subplots()
        image = ax.imshow(
            data.image,
            cmap=data.cmap,
            extent=data.extent,
            interpolation=data.interpolation,
            origin=data.origin,
        )

        ax.set_title(data.title)
        ax.set_xlabel(data.x_label)
        ax.set_ylabel(data.y_label)
        ax.set_xscale(data.xscale)
        ax.set_yscale(data.yscale)
        ax.axis(data.axis)

        if data.show_colorbar:
            fig.colorbar(image, ax=ax, label="Escape iteration")

        self._save_if_requested(fig, data)
        plt.show()

    @staticmethod
    def _save_if_requested(fig: plt.Figure, data: BasePlotData) -> None:
        if not data.save_path:
            return

        save_kwargs: dict[str, str | int] = {"dpi": data.save_dpi}
        if data.axis == "off":
            save_kwargs["bbox_inches"] = "tight"
            save_kwargs["pad_inches"] = 0

        path = Path(data.save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, **save_kwargs)
