from dataclasses import dataclass

from rich.theme import Theme


@dataclass
class UIEvent:
    pass


@dataclass
class UpdateThemeEvent(UIEvent):
    theme: Theme


@dataclass
class RenderEvent(UIEvent):
    width: int
    height: int
