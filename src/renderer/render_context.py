from dataclasses import dataclass

from rich.theme import Theme


@dataclass
class RenderContext:
    width: int
    height: int
    theme: Theme
