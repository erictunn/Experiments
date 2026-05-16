"""Basic helpers for the graph files."""

def get_cmap() -> str | None:
    """Prompts user for a colour map and returns it."""
    cmap = input(
        "Choose a colour scheme. Here are some suggetions: "
        "\n twilight_shifted"
        "\n inferno"
        "\n magma"
        "\n plasma"
        "\n spectral"
        "\n cividis"
        "\n cubehelix"
        "\n Enter nothing for twilight_shifted\n"
    )
    return None if not cmap else cmap
